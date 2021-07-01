<template>
  <div>
    <BMenu :items="bh"></BMenu>
    <v-container class="my-5">
      <v-row class="mb-5">
        <v-col
          ><h2>{{ title }}</h2></v-col
        >
        <v-col class="text-right"
          ><v-btn class="primary" @click="search()"
            ><v-icon class="mr-1">mdi-magnify</v-icon>{{ $t('search') }}</v-btn
          ></v-col
        >
      </v-row>

      <div class="mb-2">
        <b>使用上の注意</b
        >：「連」と「箱」において複数の値をチェックした場合、検索条件が同じ層になるように、子階層を選択してください。
        <ul>
          <li class="mt-2">
            <v-chip label class="mr-2 success" small>良い例</v-chip>連「1,
            2」、箱「001<small>（連1が親）</small>,
            017<small>（連2が親）</small>」
          </li>
          <li class="mt-2">
            <v-chip label class="mr-2 error" small>悪い例</v-chip>連「1,
            2」、箱「001<small>（連1が親）</small>」：
            この場合、連2の子階層が指定されていないため、連2の条件は無視されます。
          </li>
        </ul>
      </div>

      <v-row>
        <v-col cols="4">
          <v-card outlined flat>
            <v-card-title class="text-h5 text-center grey lighten-2">
              所在・連
            </v-card-title>
            <div class="pa-5">{{ $t('checked') }}: {{ rs.join(', ') }}</div>
            <v-list-item v-for="(item, key) in items" :key="key">
              <template>
                <v-list-item-action>
                  <v-checkbox v-model="rs" :value="key"></v-checkbox>
                  <!-- @change=";(h = ''), (k = [])" -->
                </v-list-item-action>

                <v-list-item-content>
                  <v-list-item-title>{{ key }}</v-list-item-title>
                </v-list-item-content>

                <v-list-item-action>
                  <template v-if="r === key">
                    <v-btn class="success" depressed @click="r = ''">
                      {{ $t('selected') }}
                    </v-btn>
                  </template>
                  <template v-else>
                    <v-btn @click="r = key">{{ $t('open') }}</v-btn>
                  </template>
                </v-list-item-action>
              </template>
            </v-list-item>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card outlined flat>
            <v-card-title class="text-h5 text-center grey lighten-2">
              所在・箱
            </v-card-title>
            <div class="pa-5">{{ $t('checked') }}: {{ hs.join(', ') }}</div>
            <template v-if="r !== ''">
              <template>
                <v-list-item
                  v-for="(item, key) in bbb(items[r])"
                  :key="`${item}-${key}`"
                >
                  <template>
                    <v-list-item-action>
                      <v-checkbox v-model="hs" :value="item"></v-checkbox>
                    </v-list-item-action>

                    <v-list-item-content>
                      <v-list-item-title>{{ item }}</v-list-item-title>
                    </v-list-item-content>

                    <v-list-item-action>
                      <template v-if="h === item">
                        <v-btn class="success" depressed @click="h = ''">
                          {{ $t('selected') }}
                        </v-btn>
                      </template>
                      <template v-else>
                        <v-btn @click="h = item">{{ $t('open') }}</v-btn>
                      </template>
                    </v-list-item-action>
                  </template>
                </v-list-item>
              </template>
            </template>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card outlined flat>
            <v-card-title class="text-h5 text-center grey lighten-2">
              所在・函
            </v-card-title>
            <div class="pa-5">{{ $t('checked') }}: {{ k.join(', ') }}</div>
            <template v-if="r !== '' && h !== ''">
              <v-list-item
                v-for="(item, key) in items[r][h]"
                :key="`${item}-${key}`"
              >
                <template>
                  <v-list-item-action>
                    <v-checkbox v-model="k" :value="item"></v-checkbox>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>{{ item }}</v-list-item-title>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </template>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import axios from 'axios'
import BMenu from '~/components/BMenu.vue'

@Component({
  components: {
    BMenu,
  },
})
export default class Page extends Vue {
  get title(): any {
    return '所在'
  }

  head() {
    return {
      title: this.title,
    }
  }

  get bh(): any[] {
    return [
      {
        text: this.$t('top'),
        disabled: false,
        to: this.localePath({ name: 'index' }),
        exact: true,
      },
      {
        text: this.$t(this.title),
      },
    ]
  }

  r: string = ''
  h: string = ''

  rs: string[] = []
  hs: string[] = []
  k: string[] = []

  items: any = {}

  async mounted() {
    let index: any = await axios.get(process.env.BASE_URL + '/data/tree.json')
    index = index.data
    this.items = index
  }

  bbb(data: any) {
    const keys = Object.keys(data)
    keys.sort()
    return keys // items
  }

  get aaa() {
    if (this.items[this.r]) {
      const data = this.items[this.r]
      const keys = Object.keys(data)
      keys.sort()
      return keys
    } else {
      return []
    }
  }

  ccc(data: any) {
    const keys = Object.keys(data)
    keys.sort()
    // return keys // items
    console.log(keys.sort())

    const map = []
    for (const key of keys) {
      map.push({
        label: key,
        value: data[key],
      })
    }
    return map
  }

  search() {
    const query: any = {}

    const rs = this.rs
    if (rs.length > 0) {
      for (let i = 0; i < rs.length; i++) {
        query[`main[refinementList][連][${i}]`] = rs[i]
      }
    }

    const hs = this.hs
    if (hs.length > 0) {
      for (let i = 0; i < hs.length; i++) {
        query[`main[refinementList][箱][${i}]`] = hs[i]
      }
    }

    const k = this.k
    if (k.length > 0) {
      for (let i = 0; i < k.length; i++) {
        query[`main[refinementList][函册次][${i}]`] = k[i]
      }
    }

    this.$router.push(
      this.localePath({
        name: 'search-slug',
        params: { slug: 'advanced' },
        query,
      })
    )
  }
}
</script>
