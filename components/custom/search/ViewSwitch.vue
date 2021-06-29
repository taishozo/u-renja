<template>
  <div>
    <v-row>
      <v-col cols="12" sm="9"></v-col>
      <v-col cols="12" sm="3">
        <v-select
          v-model="item"
          hide-details
          class="mb-0"
          outlined
          rounded
          :items="items"
          dense
          @change="changeValue()"
        ></v-select>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Prop, Vue, Component, Watch } from 'nuxt-property-decorator'

import ResultOption from '~/components/display/ResultOption.vue'

@Component({
  components: {
    ResultOption,
  },
})
export default class FullTextSearch extends Vue {
  item: string = ''

  @Prop({})
  aggs!: any

  @Watch('facets', { deep: true })
  watchV() {
    this.init()
  }

  init() {
    const facets = this.aggs
    console.log({ facets })
  }

  mounted() {
    let slug = this.$route.params.slug
    if (!slug) {
      slug = 'default'
    }
    this.item = slug

    this.init()
  }

  items: any = [
    {
      text: '所在',
      value: 'tree',
    },
    {
      text: '書名目録',
      value: 'default',
    },
    {
      text: '詳細目録',
      value: 'advanced',
    },
  ]

  changeValue() {
    const item = this.item

    if (item === 'tree') {
      this.$router.push(
        this.localePath({
          name: 'tree',
        })
      )
    } else {
      const values = this.aggs['通番'].value

      const query: any = {}
      for (let i = 0; i < values.length; i++) {
        query[`main[refinementList][通番][${i}]`] = values[i]
      }

      this.$router.push(
        this.localePath({
          name: 'search-slug',
          params: { slug: item },
          query,
        })
      )
    }
  }
}
</script>
