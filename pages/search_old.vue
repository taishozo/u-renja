<template>
  <div>
    <v-sheet color="grey lighten-3">
      <SearchFilter />
    </v-sheet>

    <v-container fluid>
      <v-row dense>
        <v-col class="py-0 my-0" cols="12" sm="6" lg="8">
          <h2 class="my-2" style="vertical-align: middle;">
            {{ $t('search_result') }}: {{ total.toLocaleString()
            }}{{ $t('hits') }}
          </h2>
        </v-col>
        <v-col class="py-0 my-0" cols="12" sm="6" lg="4">
          <v-row dense>
            <template v-if="layout_ !== 'stats'">
              <v-col class="py-0 my-0" cols="12" sm="3">
                <v-select
                  v-model="sort"
                  :items="computedItemsSort"
                  :label="$t('Sort by')"
                  @change="setSort"
                ></v-select>
              </v-col>
              <v-col class="py-0 my-0" cols="12" sm="3">
                <v-select
                  v-model="size"
                  :items="[
                    { value: 24, text: '24' },
                    { value: 60, text: '60' },
                    { value: 120, text: '120' },
                    { value: 512, text: '512' },
                  ]"
                  :label="$t('items_per_page')"
                  @change="setSize"
                ></v-select>
              </v-col>
            </template>
            <v-col class="py-0 my-0" cols="12" sm="3">
              <v-select
                v-model="layout_"
                :items="layouts"
                :label="$t('layout')"
              ></v-select>
            </v-col>
            <!-- && !mobileFlag -->
            <v-col
              v-show="
                (layout_ === 'grid' || layout_ === 'image') &&
                $vuetify.breakpoint.name != 'xs'
              "
              cols="12"
              sm="3"
              class="py-0 my-0"
            >
              <v-select
                v-model="col"
                :label="$t('col')"
                :items="[
                  { value: 1, text: '1' },
                  { value: 2, text: '2' },
                  { value: 3, text: '3' },
                  { value: 4, text: '4' },
                  { value: 6, text: '6' },
                  { value: 12, text: '12' },
                ]"
              ></v-select>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row>
        <v-col
          cols="12"
          :sm="facetFlag ? 8 : 12"
          :md="facetFlag ? 9 : 12"
          order-sm="12"
        >
          <v-row v-if="false" no-gutters align="center">
            <!--
            <v-col cols="12" sm="4"> </v-col> -->
            <!-- sm="8" -->
            <v-col cols="12" :sm="8" :lg="6" align="center"> </v-col>
          </v-row>

          <template v-if="total > 0">
            <v-row>
              <v-col cols="12" :sm="manifest != '' ? 6 : 12">
                <div
                  :style="'max-height : ' + height + 'px'"
                  class="overflow-y-auto"
                >
                  <div class="text-center my-5">
                    <v-pagination
                      v-show="layout_ !== 'stats' && layout_ !== 'map'"
                      v-model="currentPage"
                      :length="paginationLength"
                      :total-visible="7"
                      @input="setCurrentPage"
                    ></v-pagination>
                  </div>
                  <SearchResult />

                  <div class="text-center my-5">
                    <v-pagination
                      v-show="layout_ !== 'stats' && layout_ !== 'map'"
                      v-model="currentPage"
                      :length="paginationLength"
                      :total-visible="7"
                      @input="setCurrentPage"
                    ></v-pagination>
                  </div>
                </div>
              </v-col>
              <v-col
                v-if="manifest != ''"
                cols="12"
                :sm="manifest != '' ? 6 : 0"
              >
                <div class="text-right">
                  <v-btn
                    class="mb-2"
                    @click="
                      manifest = ''
                      memberId = ''
                    "
                    >{{ $t('close') }}</v-btn
                  >
                </div>
                <!-- py-2 px-2 -->
                <iframe
                  class=""
                  :src="miradorPath"
                  seamless="seamless"
                  width="100%"
                  :height="height + 'px'"
                  style="border: none;"
                  allow="fullscreen"
                ></iframe>
              </v-col>
            </v-row>
          </template>
        </v-col>

        <v-col :sm="4" :md="3" order-sm="1">
          <div :style="'max-height : ' + height + 'px'" class="overflow-y-auto">
            <template v-if="total > 0">
              <h3 class="mb-0">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <v-icon v-on="on" @click="facetFlag = !facetFlag">{{
                      facetFlag
                        ? 'mdi-arrow-collapse-left'
                        : 'mdi-arrow-collapse-right'
                    }}</v-icon>
                  </template>
                  <span>{{
                    facetFlag ? $t('close_facets') : $t('open_facets')
                  }}</span>
                </v-tooltip>
                {{ $t('refine_your_search') }}
              </h3>
              <FacetSearchOptions v-show="facetFlag" class="mt-5" />
              <!-- v-if="results.aggregations"  -->
            </template>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import SearchForm from '~/components/search/SearchForm.vue'
import SearchFilter from '~/components/search/filter.vue'
import SearchResult from '~/components/search/SearchResult.vue'
import FacetSearchOptions from '~/components/search/FacetSearchOptions.vue'

@Component({
  components: {
    SearchForm,
    SearchFilter,
    FacetSearchOptions,
    SearchResult,
  },
  watchQuery: true,
})
export default class search extends Vue {
  height: any = window.innerHeight

  get memberId() {
    return this.$store.state.currentMember
  }

  set memberId(value) {
    this.$store.commit('setCurrentMember', value)
  }

  get manifest() {
    return this.$store.state.currentManifest
  }

  set manifest(value) {
    this.$store.commit('setCurrentManifest', value)
  }

  string = ''

  get miradorPath() {
    const manifest = this.manifest
    if (manifest === '') {
      return null
    }
    const memberId: string = this.memberId
    const params = [
      {
        manifest,
        canvas: memberId,
      },
    ]
    return '/mirador/?params=' + encodeURIComponent(JSON.stringify(params))
  }

  loadingFlag: boolean = false

  // ソート項目
  sortLabelsTmp: any = process.env.SORT_LABELS
  itemsSort: string[] = []

  get results() {
    return this.$store.state.result.hits.hits
  }

  get layouts() {
    const layouts: any[] = [
      { value: 'grid', text: this.$t('grid') },
      { value: 'list', text: this.$t('list') },
      { value: 'image', text: this.$t('thumbnail') },
      { value: 'table', text: this.$t('table') },
      { value: 'stats', text: this.$t('graph') },
    ]

    return layouts
  }

  get currentPage() {
    return this.$store.state.currentPage
  }

  set currentPage(value) {
    this.$store.commit('setCurrentPage', value)
  }

  get layout_() {
    return this.$store.state.layout
  }

  set layout_(value) {
    this.$store.commit('setLayout', value)
  }

  get col() {
    return this.$store.state.col
  }

  set col(value) {
    this.$store.commit('setCol', value)
  }

  get size() {
    return this.$store.state.size
  }

  set size(value) {
    this.$store.commit('setSize', value)
  }

  get sort() {
    return this.$store.state.sort
  }

  set sort(value) {
    this.$store.commit('setSort', value)
  }

  get facetFlag() {
    return this.$store.state.facetFlag
  }

  set facetFlag(value) {
    this.$store.commit('setFacetFlag', value)
  }

  async fetch(context: any) {
    const store = context.store
    const state = store.state

    // ------ インデックス ---------

    if (state.index == null) {
      const uri = context.query.u
      if (!uri) {
        /*
        location.href =
          'https://github.com/nakamura196/icc2/blob/master/README.md'
        */
        return
      }
      const index = await context.app.$searchUtils.createIndex(uri)
      context.app.$searchUtils.initStore(store, index)
    }

    // ------ ファセット ---------

    if (Object.keys(state.facetLabels)) {
      const index: any = store.state.index

      const facetLabels: any = {}
      const facetFlags: string[] = []

      const keys: string[] = Object.keys(index).sort()

      for (let i = 0; i < keys.length; i++) {
        const field = keys[i]

        facetLabels[field] = field
        if (!field.startsWith('_')) {
          facetFlags.push(field)
        }
      }

      // ファセット項目
      /*
      const facetLabels: any = process.env.FACETS_LABELS
      store.commit('setFacetLabels', JSON.parse(facetLabels))
      const facetFlags: any = process.env.FACETS_FLAGS
      store.commit('setFacetFlags', JSON.parse(facetFlags))
      */

      store.commit('setFacetLabels', facetLabels)
      store.commit('setFacetFlags', facetFlags)
    }

    // ------ 検索 ---------

    const routeQuery = context.query

    const esQuery = context.app.$searchUtils.createQuery(routeQuery, state)
    store.commit('setQuery', esQuery)

    const result = context.app.$searchUtils.search(
      store.state.index,
      store.state.data,
      store.state.query
    )

    context.store.commit('setResult', result)

    // --------

    store.commit('init')

    const keywords: any = routeQuery.keyword
    if (keywords) {
      store.commit('setKeyword', keywords)
    }

    for (const key in routeQuery) {
      const types = ['fc', 'q']
      for (let t = 0; t < types.length; t++) {
        const type = types[t]
        if (key.includes(type + '-')) {
          store.commit('setAdvanced', {
            label: key,
            values: routeQuery[key],
            type,
          })
        }
      }

      /*
      if (key.includes('fc-')) {
        store.commit('setFc', {
          label: key,
          values: routeQuery[key],
        })
      }
      */
    }

    const layout: any = routeQuery.layout
    if (layout) {
      store.commit('setLayout', layout)
    }

    const sort: any = routeQuery.sort
    if (sort) {
      store.commit('setSort', sort)
    }

    const from: any = routeQuery.from
    if (from) {
      store.commit('setFrom', Number(from))
    }

    const size: any = routeQuery.size
    if (size) {
      store.commit('setSize', Number(size))
    }

    const currentPage = state.from / state.size + 1
    store.commit('setCurrentPage', currentPage)

    if (process.browser) {
      window.scrollTo(0, 0)
    }
  }

  // ------ Watch -------

  @Watch('layout_')
  watchLayout(currentValue: string): void {
    if (
      (currentValue === 'image' || currentValue === 'stats') &&
      this.facetFlag
    ) {
      this.facetFlag = !this.facetFlag
    } else if (
      currentValue !== 'image' &&
      currentValue !== 'stats' &&
      !this.facetFlag
    ) {
      this.facetFlag = !this.facetFlag
    }
  }

  // ------ 関数 -------

  setCurrentPage() {
    if (this.currentPage > 0) {
      const query: any = Object.assign({}, this.$route.query)
      query.from = (this.currentPage - 1) * this.size
      this.updateQuery(query)
    }
  }

  setSize() {
    const query: any = Object.assign({}, this.$route.query)
    query.from = 0
    query.size = this.size
    this.updateQuery(query)
  }

  setSort() {
    const query: any = Object.assign({}, this.$route.query)
    query.from = 0
    query.sort = this.sort
    this.updateQuery(query)
  }

  updateQuery(query: any) {
    this.$router.push(
      this.localePath({
        name: 'search',
        query,
      }),
      () => {},
      () => {}
    )
  }

  get total(): number {
    const result = this.$store.state.result
    if (result.hits) {
      return result.hits.total.value
    } else {
      return 0
    }
  }

  get paginationLength() {
    return Math.ceil(this.total / this.size)
  }

  get computedItemsSort() {
    if (!this.$store.state.index) {
      return []
    }
    const arr: any[] = [
      {
        value: '_score:desc',
        text: this.$t('relevance'),
      },
    ]

    const orders = ['asc', 'desc']

    const itemsSort = Object.keys(this.$store.state.index).sort() // this.itemsSort

    for (let i = 0; i < itemsSort.length; i++) {
      const value = itemsSort[i]
      if (value === '_full_text') {
        continue
      }
      for (let j = 0; j < orders.length; j++) {
        const order = orders[j]
        const label = value.startsWith('_') ? value.slice(1) : value
        arr.push({
          value: value + '.keyword:' + order,
          text: label + ' ' + this.$t(order),
        })
      }

      if (i === 0 && this.sort == null) {
        this.sort = value + '.keyword:asc'
      }
    }

    return arr
  }
}
</script>
