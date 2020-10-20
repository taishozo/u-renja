<template>
  <div>
    <table border="1" style="border-collapse: collapse;" width="100%">
      <thead>
        <tr>
          <th>連</th>
          <th>箱</th>
          <th>段</th>
          <th>冊</th>
          <th>闕</th>
          <th>函册次</th>
          <th>經番</th>
          <th>通番</th>
          <th>枝番</th>
          <th>千字文</th>
          <th>經典名稱</th>
          <th>卷次等</th>
          <th>丁數</th>
          <th>卷末附録</th>
          <th>刊記</th>
          <th>圖像</th>
          <th>詳細情報</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(obj, index) in items" :key="index">
          <td>{{ $utils.formatArrayValue(obj.raw._source['連']) }}</td>
          <td>{{ Number($utils.formatArrayValue(obj.raw._source['箱'])) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['段']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['冊']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['闕']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['函册次']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['經番']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['通番']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['枝番']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['千字文']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['經典名稱']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['卷次等']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['丁數']) }}</td>
          <td>
            {{ $utils.formatArrayValue(obj.raw._source['卷末附録_facet']) }}
          </td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['刊記']) }}</td>
          <td>{{ $utils.formatArrayValue(obj.raw._source['圖像']) }}</td>
          <td>
            <nuxt-link
              target="_blank"
              :to="
                localePath({
                  name: 'item-id',
                  params: {
                    id: obj.id.split('/iiif/')[1].replace('/manifest.json', ''),
                  },
                })
              "
              >{{ 'more' }}
            </nuxt-link>
          </td>
        </tr>
      </tbody>
    </table>
    <!--
    <v-data-table :headers="headers" :items="items" hide-default-footer>
      <template v-slot:item.image="{ item }">
        <nuxt-link
          class="mb-4"
          :to="
            localePath({
              name: 'item',
              query: { id: item.id, u: $route.query.u },
            })
          "
        >
          <v-img
            :src="item.image"
            contain
            style="height: 90px; width: 90px;"
            class="grey lighten-2 my-2"
          ></v-img>
        </nuxt-link>
      </template>

      <template v-slot:item.label="{ item }">
        <nuxt-link
          class="mb-4"
          :to="
            localePath({
              name: 'item',
              query: { id: item.id, u: $route.query.u },
            })
          "
        >
          <span v-html="item.label"></span>
        </nuxt-link>
      </template>

      <template v-slot:item.icons="{ item }">
        <ResultOption
          :item="{
            label: $utils.formatArrayValue(item.raw._source._label),
            manifest: $utils.formatArrayValue(item.raw._source._manifest),
            url: encodeURIComponent(getUrl(item.raw)),
            id: item.id,
          }"
        />
      </template>
    </v-data-table>
    -->
  </div>
</template>

<script lang="ts">
import { Vue, Watch, Component } from 'nuxt-property-decorator'
import axios from 'axios'
import ResultOption from '~/components/display/ResultOption.vue'

@Component({
  components: {
    ResultOption,
  },
})
export default class TableSearchResult extends Vue {
  flg1: boolean = false
  flg2: boolean = false

  iiifMap: any = {}

  get results() {
    return this.$store.state.result.hits.hits
  }

  items: any[] = []
  fields!: any[]

  headers: any[] = []

  @Watch('results', { deep: true })
  watchTmp() {
    this.main()
  }

  async mounted() {
    const self = this
    await axios
      .get(
        'https://d1av1vcgsldque.cloudfront.net/iiif/collection/%E9%85%89%E8%93%AE%E7%A4%BE%E7%94%BB%E5%83%8F.json'
      )
      .then(function (data) {
        const collection = data.data
        const manifests = collection.manifests
        const map: any = {}
        for (let i = 0; i < manifests.length; i++) {
          const manifest = manifests[i]
          const tmp = manifest.thumbnail.split('/')
          map[tmp[tmp.length - 2]] = manifest['@id']
        }
        self.iiifMap = map
      })

    const facetLabels: any = this.$store.state.facetLabels
    const fields: any = [
      { key: 'image', label: '' },
      { key: 'label', label: this.$t('title') },
    ]
    for (const field in facetLabels) {
      fields.push({
        key: field,
        label: field,
      })
    }
    fields.push({ key: 'icons', label: '' })
    this.fields = fields

    const headers = []
    for (let i = 0; i < fields.length; i++) {
      const field = fields[i]
      if (field.label.startsWith('_')) {
        continue
      }
      headers.push({
        text: field.label,
        align: 'start',
        value: field.key,
      })
    }
    this.headers = headers

    this.main()
  }

  main() {
    const fields = this.fields
    const results = this.results
    const items: any[] = []
    for (let i = 0; i < results.length; i++) {
      const result: any = results[i]
      const item: any = {
        image: this.$utils.formatArrayValue(result._source._thumbnail),
        label: this.$utils.formatArrayValue(result._source._label),
        id: result._id,
        raw: result,
      }

      for (let j = 0; j < fields.length; j++) {
        const label = fields[j].key
        if (result._source[label]) {
          item[label] = this.$utils.truncate(
            this.$utils.formatArrayValue(result._source[label]),
            50
          )
        }
      }
      items.push(item)
    }
    this.items = items
  }

  getUrl(item: any) {
    return (
      process.env.BASE_URL +
      this.localePath({
        name: 'item',
        query: {
          u: this.$route.query.u,
          id: item._id,
        },
      })
    )
  }

  bunrui(obj: any) {
    return (
      this.$utils.formatArrayValue(obj.raw._source['分類(1)']) +
      ' ' +
      this.$utils.formatArrayValue(obj.raw._source['分類(2)']) +
      ' ' +
      this.$utils.formatArrayValue(obj.raw._source['分類(3)'])
    )
  }

  tana(obj: any) {
    return (
      this.$utils.formatArrayValue(obj.raw._source['函册']) +
      (obj.raw._source['函册(to)']
        ? '~' + this.$utils.formatArrayValue(obj.raw._source['函册(to)'])
        : '') +
      this.$utils.formatArrayValue(obj.raw._source['函册(闕)'])
    )
  }

  size(obj: any) {
    return (
      this.$utils.formatArrayValue(obj.raw._source['寸法(縦）']) +
      '×' +
      this.$utils.formatArrayValue(obj.raw._source['寸法(横)']) +
      '(' +
      this.$utils.formatArrayValue(obj.raw._source['寸法（計測箇所）']) +
      ')'
    )
  }

  status(obj: any) {
    const results = []

    for (let i = 1; i < 5; i++) {
      const label = i === 1 ? '大正藏經典番號' : '大正藏經典番号'

      if (!obj.raw._source[label + '(' + i + ')']) {
        continue
      }
      results.push(
        '<a href="https://taishozo.github.io/db/search?keyword=' +
          this.$utils.formatArrayValue(obj.raw._source[label + '(' + i + ')']) +
          '" target="_blank">' +
          this.$utils.formatArrayValue(obj.raw._source[label + '(' + i + ')']) +
          this.$utils.formatArrayValue(
            obj.raw._source['大正藏採録種別(' + i + ')']
          ) +
          '(' +
          this.$utils.formatArrayValue(
            obj.raw._source['大正藏脚注テキスト標準名称(' + i + ')']
          ) +
          ')' +
          '</a>'
      )
    }
    return results.join('<br/>')
  }

  icons(obj: any) {
    const results = []
    for (let i = 1; i < 5; i++) {
      if (!obj.raw._source['画像フォルダ名(' + i + ')']) {
        continue
      }
      const text =
        '<a href="http://www.kanzaki.com/works/2016/pub/image-annotator?u=' +
        this.iiifMap[
          this.$utils.formatArrayValue(obj.raw._source['画像フォルダ名(1)'])
        ] +
        '" target="_blank"><img width="30px" src="https://pbs.twimg.com/profile_images/596366309601845248/2uaPY5NH.png"/></a>'
      results.push(text)
    }
    return results.join('  ')
  }
}
</script>
