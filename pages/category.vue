<template>
  <div>
    <v-sheet color="grey lighten-3">
      <v-container class="py-4">
        <h1>
          <template v-if="$i18n.locale === 'ja'">
            {{ label.startsWith('_') ? $t(label) : label }}を一覧する
          </template>
          <template v-else>
            {{ $t('browse_by') }}
            {{ label.startsWith('_') ? $t(label) : label }}
          </template>
          <!-- 
          <template v-if="results.length != 2000">
            &nbsp;({{ total.toLocaleString() }})
          </template>
          -->
        </h1>
      </v-container>
    </v-sheet>

    <!-- text color="primary" -->

    <v-container>
      <v-btn
        v-for="(value, index) in map"
        :key="index"
        class="ma-1"
        :to="
          localePath({
            name: 'category',
            query: {
              field: value,
              u: $route.query.u,
            },
          })
        "
      >
        {{ value.startsWith('_') ? $t(value) : value }}
      </v-btn>

      <v-sheet color="grey lighten-3 py-1 px-3 my-5">
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
// import axios from 'axios'

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

    // const routeQuery = context.query

    let label: any = this.$route.query.field

    /*
    if (label === '_label') {
      label = this.$t(label)
    }
    */

    const map: string[] = []
    const facetLabels = state.facetLabels

    for (const field in facetLabels) {
      if (field === '_label' || !field.startsWith('_')) {
        map.push(field)
      }
    }

    if (!label) {
      label = map[0]
    }

    const aggs: any = {}
    aggs[label] = {
      terms: {
        field: label + '.keyword',
        order: {
          _count: 'desc',
        },
      },
    }

    const esQuery = {
      aggs,
    }
    store.commit('setQuery', esQuery)

    const result = this.$searchUtils.search(
      store.state.index,
      store.state.data,
      store.state.query
    )

    const buckets = result.aggregations[label].buckets
    const results = []
    for (let i = 0; i < buckets.length; i++) {
      const aggs: { [key: string]: string[] } = {}
      aggs[label] = [buckets[i].key]
      results.push({
        label: buckets[i].key,
        count: buckets[i].doc_count,
      })
    }

    this.results = results
    this.map = map
    this.label = label
  }

  head() {
    return {
      title: this.$t('category') + ' : ' + this.$t(this.label),
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.$t('search_by_category'),
        },
      ],
    }
  }

  mounted() {
    this.init()
  }

  getQuery(arr: any[]): { [key: string]: string } {
    const result: { [key: string]: string } = {}
    for (let i = 0; i < arr.length; i++) {
      const obj = arr[i]
      result[obj.field] = obj.value
    }
    return result
  }

  search() {
    const query: any = JSON.parse(JSON.stringify(this.$route.query)) // 重要
    query['size-fc'] = this.size
    this.$router.push(
      this.localePath({
        name: 'category-slug',
        params: { slug: this.title },
        query,
      }),
      () => {},
      () => {}
    )
  }

  get total() {
    let total = 0
    for (let i = 0; i < this.results.length; i++) {
      total += this.results[i].count
    }
    return total
  }

  initSizeFc() {
    const query = JSON.parse(JSON.stringify(this.$route.query)) // 重要
    query['size-fc'] = '50'
    return query
  }
}
</script>
