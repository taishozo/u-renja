<template>
  <div>
    <v-sheet color="grey lighten-3">
      <v-container class="py-4">
        <h1>
          {{ label }}
        </h1>
      </v-container>
    </v-sheet>

    <v-container>
      <!--
      <template>
        <v-btn
          v-for="(value, index) in map"
          :key="index"
          class="ma-1"
          :to="
            localePath({
              name: 'entity',
              query: {
                field: value,
                u: $route.query.u,
              },
            })
          "
        >
          {{ value }}
        </v-btn>
      </template>
      -->

      <v-row class="pa-4 mb-5">
        <v-col cols="12" sm="3" class="mb-4">
          <v-img
            :src="image"
            contain
            style="height: 150px;"
            width="100%"
            class="grey lighten-2"
          ></v-img>
        </v-col>
        <v-col cols="12" sm="9">
          <p>{{ description }}</p>

          <p>
            <v-btn
              color="primary"
              :to="
                localePath({
                  name: 'search',
                  query: getQuery(label),
                })
              "
            >
              {{ $t('search') }}
            </v-btn>
          </p>
        </v-col>
      </v-row>
    </v-container>

    <v-container fluid>
      <div v-for="(obj, index) in result" :key="index" cols="12" sm="4">
        <h3 class="my-4">{{ obj.property }}</h3>
        <HorizontalEntities :key="obj.property" :data="obj.children" />
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import axios from 'axios'
import HorizontalEntities from '~/components/display/HorizontalEntities.vue'
@Component({
  components: {
    HorizontalEntities,
  },
})
export default class PageCategory extends Vue {
  @Watch('$route', { deep: true })
  watchTmp(): void {
    this.init()
  }

  image: string = ''
  label: string = ''
  description: string = ''

  field: any = ''

  map: string[] = []

  async init() {
    const store = this.$store
    const state = store.state

    if (state.index == null) {
      const uri: any = this.$route.query.u
      const index = await this.$searchUtils.createIndex(uri)
      this.$searchUtils.initStore(store, index)
    }

    this.field = this.$route.query.field

    this.image = ''
    this.label = ''
    this.description = ''

    this.result = []

    /*

    let label: any = this.$route.query.field
    if (label === '_label') {
      label = this.$t(label)
    }

    label = 'schema:creator'
    */

    const uri: any = this.$route.query.uri
    const data: any = await this.api2(uri)
    this.image = data['schema:image'] ? data['schema:image'][0]['@id'] : ''
    this.label = data['rdfs:label'] ? data['rdfs:label'][0]['@value'] : ''
    if (data['schema:description'] && data['schema:description'].length > 0) {
      this.description = data['schema:description'][0]['@value']
    }

    for (const key in data) {
      if (
        key !== 'schema:description' &&
        key !== 'rdfs:label' &&
        key !== '@id' &&
        key !== '@context' &&
        key !== 'schema:image' &&
        key !== 'schema:name'
      ) {
        const ids = []
        const arr = data[key]
        for (let i = 0; i < arr.length; i++) {
          ids.push(arr[i]['@id'])
        }
        this.api(key, ids)
      }
    }

    this.api4(uri)

    const map: string[] = []
    const entity = store.state.entity
    for (const property in entity) {
      map.push(property)
    }
    this.map = map
  }

  head() {
    return {
      title: this.$t('entity') + ' : ' + this.$t(this.label),
    }
  }

  mounted() {
    this.init()
  }

  result: any = []

  async api2(uri: string) {
    const endpoint: string = this.$store.state.api
    const result = await axios.get(endpoint).then(function (data) {
      const result = data.data
      for (let i = 0; i < result.length; i++) {
        const obj = result[i]
        if (obj['@id'] === uri) {
          return obj
        }
      }
    })
    return result
  }

  api(property: string, uris: string[]) {
    const endpoint: string = this.$store.state.api
    const self = this
    axios.get(endpoint).then(function (data) {
      const result = data.data

      const map: any = {}

      for (let i = 0; i < result.length; i++) {
        const obj = result[i]
        // const values = obj[property]
        map[obj['@id']] = obj
      }

      const children: any[] = []
      for (let j = 0; j < uris.length; j++) {
        const id = uris[j]
        const obj = map[id]

        if (!obj) {
          continue
        }

        const newObj: any = {
          _id: obj['@id'],
          _source: {
            _label: [obj['rdfs:label'][0]['@value']],
          },
        }

        if (obj['schema:image']) {
          newObj._source._thumbnail = [obj['schema:image'][0]['@id']]
        }

        if (obj['schema:description']) {
          newObj._source._description = [obj['schema:description'][0]['@value']]
        }
        children.push(newObj)
      }

      const parent = map[uris[0]]

      self.result.push({
        parent,
        property,
        children,
      })
    })
  }

  api4(uri: string) {
    const endpoint: string = this.$store.state.api
    const self = this
    axios.get(endpoint).then(function (data) {
      const result = data.data

      const map: any = {}

      for (let i = 0; i < result.length; i++) {
        const obj = result[i]
        for (const property in obj) {
          const arr = obj[property]
          for (let j = 0; j < arr.length; j++) {
            if (arr[j]['@id'] === uri) {
              const newObj: any = {
                _id: obj['@id'],
                _source: {
                  _label: [obj['rdfs:label'][0]['@value']],
                },
              }

              if (obj['schema:image']) {
                newObj._source._thumbnail = [obj['schema:image'][0]['@id']]
              }

              if (obj['schema:description']) {
                newObj._source._description = [
                  obj['schema:description'][0]['@value'],
                ]
              }

              if (!map[property]) {
                map[property] = {
                  property: 'is ' + property + ' of',
                  children: [],
                }
              }
              map[property].children.push(newObj)
            }
          }
        }
      }

      for (const property in map) {
        self.result.push(map[property])
      }
    })
  }

  api3(property: string, uri: string) {
    const endpoint: string = this.$store.state.api
    const self = this
    axios.get(endpoint).then(function (data) {
      const result = data.data
      let parent: any = null
      for (let i = 0; i < result.length; i++) {
        const obj = result[i]
        if (obj['@id'] === uri) {
          parent = obj
        }
      }

      const children: any[] = []

      for (let i = 0; i < result.length; i++) {
        const obj = result[i]
        const values = obj[property]
        if (values && values.length > 0) {
          if (
            values[0]['@id'] === uri &&
            obj['@id'] !== self.$route.query.uri
          ) {
            const newObj: any = {
              _id: obj['@id'],
              _source: {
                _thumbnail: [obj['schema:image'][0]['@id']],
                _label: [obj['rdfs:label'][0]['@value']],
                _description: [obj['schema:description'][0]['@value']],
              },
            }
            children.push(newObj)
          }
        }
      }

      self.result.push({
        parent,
        children,
      })
    })
  }

  getQuery(label: string) {
    const result: any = {
      u: this.$route.query.u,
    }
    result['fc-' + /* this.field */ 'schema:subject'] = label
    return result
  }
}
</script>
