<template>
  <div>
    <Metadata v-if="metadata" :metadata="metadata" />
  </div>
</template>

<script lang="ts">
import { Vue, Watch, Component } from 'nuxt-property-decorator'
import Metadata from '~/components/item/Metadata.vue'

@Component({
  components: {
    Metadata,
  },
})
export default class Item extends Vue {
  metadata: any = null

  tab: string = ''

  uri: string = ''
  url: string = location.href
  title: string = ''
  id: string = ''

  async fetch(context: any) {
    const store = context.store
    const state = store.state

    if (state.index == null) {
      const uri = context.query.u
      const index = await context.app.$searchUtils.createIndex(uri)
      context.app.$searchUtils.initStore(store, index)
    }
  }

  created() {
    this.init()
  }

  init() {
    const itemId = this.$route.query.id
    const data = this.$store.state.data
    let metadata = null
    for (let i = 0; i < data.length; i++) {
      const id = data[i]._id
      if (id === itemId) {
        metadata = data[i]
      }
    }
    this.metadata = metadata

    if (process.browser) {
      window.scrollTo(0, 0)
    }
  }

  @Watch('$route', { deep: true })
  watchId(): void {
    this.init()
  }

  /*
  sorted(source: any) {
    const obj: any = {}
    const keys = Object.keys(source) // .sort()
    for (let i = 0; i < keys.length; i++) {
      const key = keys[i]
      obj[key] = source[key]
    }
    return obj
  }
  */
}
</script>
