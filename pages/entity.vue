<template>
  <div>
    <v-sheet color="grey lighten-3">
      <v-container class="py-4">
        <h1>
          <template v-if="$i18n.locale === 'ja'">
            {{ label }}を一覧する
          </template>
          <template v-else> {{ $t('browse_by') }} {{ label }} </template>
          <!-- 
          <template v-if="results.length != 2000">
            &nbsp;({{ total.toLocaleString() }})
          </template>
          -->
          <template> &nbsp;({{ result.length.toLocaleString() }}) </template>
        </h1>
      </v-container>
    </v-sheet>

    <!-- text color="primary" -->

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

      <v-row>
        <v-col v-for="(obj, index) in result" :key="index" cols="12" sm="3">
          <v-card no-body class="mb-4">
            <nuxt-link
              class="mr-2"
              :to="
                localePath({
                  name: 'detail',
                  query: {
                    u: $route.query.u,
                    uri: obj['@id'],
                    field: label,
                  },
                })
              "
            >
              <v-img
                :src="obj['schema:image'] ? obj['schema:image'][0]['@id'] : ''"
                contain
                style="height: 150px;"
                width="100%"
                class="grey lighten-2"
              ></v-img>
            </nuxt-link>

            <div class="pa-4" style="height: 100px; overflow-y: auto;">
              <nuxt-link
                class="mr-2"
                :to="
                  localePath({
                    name: 'detail',
                    query: {
                      u: $route.query.u,
                      uri: obj['@id'],
                      field: label,
                    },
                  })
                "
              >
                <!-- eslint-disable-next-line vue/no-v-html -->
                <b
                  v-if="obj['rdfs:label']"
                  v-html="obj['rdfs:label'][0]['@value']"
                ></b>
              </nuxt-link>
              <template v-if="obj['schema:description']">
                <div class="mt-2">
                  {{ obj['schema:description'][0]['@value'] }}
                </div>
              </template>
            </div>

            <template>
              <v-divider />

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                  color="primary"
                  :to="
                    localePath({
                      name: 'search',
                      query: getQuery(obj),
                    })
                  "
                >
                  {{ $t('search') }}
                </v-btn>
              </v-card-actions>
            </template>
          </v-card>
        </v-col>
      </v-row>

      <v-sheet v-if="false" color="grey lighten-3 py-1 px-3 my-5">
        <v-row dense align="center">
          <v-col cols="12" sm="4" class="py-3"
            ><h3>
              {{ results.length.toLocaleString() }}{{ $t('hits') }}
            </h3></v-col
          >
        </v-row>
      </v-sheet>

      <v-row class="mb-5">
        <v-col
          v-for="(obj, index) in results"
          :key="index"
          :cols="6"
          :sm="2"
          class="my-2"
          style="word-break: break-word;"
        >
          <!-- {{ index + 1 }}.&nbsp; -->
          <nuxt-link
            class="mr-2"
            :to="
              localePath({
                name: 'search',
                query: getQuery([
                  {
                    field: 'fc-' + label,
                    value: obj.label,
                  },
                  {
                    field: 'u',
                    value: $route.query.u,
                  },
                ]),
              })
            "
          >
            {{ obj.label }}
          </nuxt-link>
          ({{ Number(obj.count).toLocaleString() }})
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import axios from 'axios'

@Component({
  // watchQuery: true,
})
export default class PageCategory extends Vue {
  @Watch('$route', { deep: true })
  watchTmp(): void {
    this.init()
  }

  results: any[] = []
  label: string = ''
  title: string = ''

  size: number = -1

  map: string[] = []

  async init() {
    this.result = []

    const store = this.$store
    const state = store.state

    if (state.index == null) {
      const uri: any = this.$route.query.u
      const index = await this.$searchUtils.createIndex(uri)
      this.$searchUtils.initStore(store, index)
    }

    if (Object.keys(state.facetLabels)) {
      const index: any = store.state.index

      const facetLabels: any = {}
      const facetFlags: string[] = []

      const keys: string[] = Object.keys(index) // .sort()

      for (let i = 0; i < keys.length; i++) {
        const field = keys[i]

        facetLabels[field] = field
        if (!field.startsWith('_')) {
          facetFlags.push(field)
        }
      }

      store.commit('setFacetLabels', facetLabels)
      store.commit('setFacetFlags', facetFlags)
    }

    let label: any = this.$route.query.field
    if (!label) {
      label = 'schema:subject'
    }
    /*
    if (label === '_label') {
      label = this.$t(label)
    }
    */

    const map: string[] = []

    for (const field in map) {
      if (field === '_label' || !field.startsWith('_')) {
        map.push(field)
      }
    }

    const entity = store.state.entity
    for (const property in entity) {
      map.push(property)
    }

    const entities = store.state.entity[label]

    for (const uri in entities) {
      this.api(uri)
    }

    this.map = map
    this.label = label
  }

  head() {
    return {
      title: this.$t('entity') + ' : ' + this.label, // this.$t(this.label)
    }
  }

  mounted() {
    this.init()
  }

  result: any = []

  api(uri: string) {
    const self: any = this
    const endpoint: string = this.$store.state.api
    axios.get(endpoint).then(function (data) {
      const result = data.data
      for (let i = 0; i < result.length; i++) {
        const obj = result[i]
        if (obj['@id'] === uri) {
          self.result.push(obj)
        }
      }
    })
  }

  getQuery(obj: any) {
    const result: any = {
      u: this.$route.query.u,
    }
    result['fc-' + this.label] = obj['rdfs:label']
      ? obj['rdfs:label'][0]['@value']
      : ''
    return result
  }
}
</script>
