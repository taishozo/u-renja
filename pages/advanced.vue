<template>
  <div>
    <v-row dense>
      <v-col
        v-if="facetFlag"
        cols="12"
        :sm="facetFlag ? 4 : 0"
        :md="facetFlag ? 3 : 0"
      >
        <div
          :style="'height: ' + (height - (64 + 10)) + 'px'"
          class="overflow-y-auto pa-4"
        >
          <v-sheet color="grey lighten-3">
            <SearchFilter class="mb-4" />
          </v-sheet>
          <template v-if="total > 0">
            <h3 class="mb-0">
              <!--
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
              -->
              {{ $t('refine_your_search') }}
            </h3>
            <FacetSearchOptions v-show="facetFlag" class="mt-5" />
            <!-- v-if="results.aggregations"  -->
          </template>
        </div></v-col
      >
      <v-col cols="12" :sm="facetFlag ? 8 : 12" :md="facetFlag ? 9 : 12">
        <v-row dense>
          <v-col cols="12" :sm="manifest != '' ? 7 : 12">
            <div
              :style="'height: ' + (height * 0.99 - (64 + 10)) + 'px'"
              class="overflow-y-auto pa-4"
            >
              <v-row dense>
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
                  {{ $t('search_result') }}: {{ total.toLocaleString()
                  }}{{ $t('hits') }}
                </h3>
                <v-col class="mt-4" cols="12">
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

              <template v-if="total > 0">
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
              </template>
            </div>
          </v-col>
          <v-col v-if="manifest != ''" cols="12" :sm="manifest != '' ? 5 : 0">
            <div
              :style="'height: ' + (height * 0.99 - (64 + 10)) + 'px'"
              class="overflow-y-auto pa-4"
            >
              <iframe
                class=""
                :src="miradorPath"
                seamless="seamless"
                width="100%"
                :height="height * 0.8 + 'px'"
                style="border: none;"
                allow="fullscreen"
              ></iframe>
              <div class="text-right">
                <v-btn
                  class="mt-2 mb-2"
                  color="primary"
                  @click="
                    manifest = ''
                    memberId = ''
                  "
                  >{{ $t('close') }}</v-btn
                >
              </div>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'
import SearchForm from '~/components/search/SearchForm.vue'
import SearchFilter from '~/components/search/Filter.vue'
import SearchResult from '~/components/search/SearchResult2.vue'
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

  baseUrl: any = process.env.BASE_URL

  mounted() {
    // this.height -= document.getElementById('head').style.height
  }

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

    const param: any = {
      manifest,
    }
    // 要検討
    if (memberId !== manifest) {
      param.canvas = memberId
    }
    const params = [param]
    return (
      this.baseUrl +
      '/mirador/?params=' +
      encodeURIComponent(JSON.stringify(params))
    )
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
    const startTime = Date.now() // 開始時間

    const store = context.store
    const state = store.state

    // 初期化
    store.commit('setCurrentManifest', '')

    const uri = process.env.BASE_URL + '/iiif/collection/advanced.json'
    const index = await context.app.$searchUtils.createIndex(uri)
    context.app.$searchUtils.initStore(store, index)

    let endTime = Date.now() // 終了時間
    console.log('indexing', endTime - startTime) // 何ミリ秒かかったかを表示する

    // ------ ファセット ---------

    const facetLabels: any = {
      連: '所在一覧-連',
      箱: '所在一覧-箱',
      '函(通番)': '所在一覧-函',
      '分類(1)': '分類(1)',
      '分類(2)': '分類(2)',
      '分類(3)': '分類(3)',
      函册次: '函册次',
      經番: '經番',
      通番: '通番',
      '刊記(西暦年)': '刊記(西暦年)',
      圖像: '圖像',
    }
    const facetFlags: string[] = []

    for (const key in facetLabels) {
      facetFlags.push(key)
    }

    store.commit('setFacetLabels', facetLabels)
    store.commit('setFacetFlags', facetFlags)

    // ------ 検索 ---------

    const routeQuery = context.query

    const esQuery = context.app.$searchUtils.createQuery(routeQuery, state)
    store.commit('setQuery', esQuery)

    const result = context.app.$searchUtils.search(
      store.state.index,
      store.state.data,
      store.state.query
    )

    endTime = Date.now() // 終了時間
    console.log('searched', endTime - startTime) // 何ミリ秒かかったかを表示する

    context.store.commit('setResult', result)

    endTime = Date.now() // 終了時間
    console.log('commit', endTime - startTime) // 何ミリ秒かかったかを表示する

    // --------

    store.commit('init')

    endTime = Date.now() // 終了時間
    console.log('init', endTime - startTime) // 何ミリ秒かかったかを表示する

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

    endTime = Date.now() // 終了時間
    console.log('fetch end', endTime - startTime) // 何ミリ秒かかったかを表示する
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
        value: '通番.keyword:asc',
        text: this.$t('通番 昇順'),
      },
      {
        value: '通番.keyword:desc',
        text: this.$t('通番 降順'),
      },
    ]

    /*
    const arr: any[] = [
      {
        value: '_score:desc',
        text: this.$t('relevance'),
      },
      {
        value: '_random:desc',
        text: this.$t('random'),
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
    */

    return arr
  }

  text =
    ' <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head> <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head> <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head> <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head> <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head> <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head> <link rel="preload" href="/runtime~app.9e334eaa15688c4b1249.js" as="script"><link rel="preload" href="/common.e61b5424e4663448f46c.css" as="style"><link rel="preload" href="/vendors~app.e61b5424e4663448f46c.js" as="script"><link rel="preload" href="/common.950630d7145f9aa5224d.css" as="style"><link rel="preload" href="/app.950630d7145f9aa5224d.js" as="script"><link rel="preload" href="/layout-root-Index.9902e555ebf8f251f7d2.js" as="script"><link rel="preload" href="/layout-documentation-Index.79f7b3be2dfbb8983e70.js" as="script"><link rel="preload" href="/common.b4fe1dc57429f7fff241.css" as="style"><link rel="preload" href="/1485.b4fe1dc57429f7fff241.js" as="script"><link rel="preload" href="/common.f41e999ee1a08efaa008.css" as="style"><link rel="preload" href="/1447.f41e999ee1a08efaa008.js" as="script"><link rel="preload" href="/1666.bd28631bc9a4931eefd8.js" as="script"><link rel="preload" href="/1668.aa0c942993a126b2d8fc.js" as="script"><link rel="preload" href="/1664.ebba05acee86095e1fd7.js" as="script"><link rel="preload" href="/common.2ef87f5b8f92941cac3a.css" as="style"><link rel="preload" href="/1483.2ef87f5b8f92941cac3a.js" as="script"><link rel="preload" href="/1665.6343ca474931c2bf3246.js" as="script"><link rel="preload" href="/common.53d1c392fc334c5d7186.css" as="style"><link rel="preload" href="/1486.53d1c392fc334c5d7186.js" as="script"><link rel="preload" href="/1667.1d5caaccb431e373e583.js" as="script"><link rel="stylesheet" href="/common.e61b5424e4663448f46c.css"><link rel="stylesheet" href="/common.950630d7145f9aa5224d.css"><link rel="stylesheet" href="/common.b4fe1dc57429f7fff241.css"><link rel="stylesheet" href="/common.f41e999ee1a08efaa008.css"><link rel="stylesheet" href="/common.2ef87f5b8f92941cac3a.css"><link rel="stylesheet" href="/common.53d1c392fc334c5d7186.css"></head>'
}
</script>
