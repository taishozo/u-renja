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

      <v-row>
        <v-col cols="4">
          <v-card outlined flat>
            <v-card-title class="text-h5 text-center grey lighten-2">
              所在・連
            </v-card-title>
            <v-list-item v-for="(item, key) in items" :key="key">
              <template>
                <v-list-item-action>
                  <v-checkbox
                    v-model="r"
                    :value="key"
                    @change=";(h = ''), (k = '')"
                  ></v-checkbox>
                </v-list-item-action>

                <v-list-item-content>
                  <v-list-item-title>{{ key }}</v-list-item-title>
                </v-list-item-content>
              </template>
            </v-list-item>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card outlined flat>
            <v-card-title class="text-h5 text-center grey lighten-2">
              所在・箱
            </v-card-title>
            <template v-if="r !== ''">
              <v-list-item v-for="(item, key) in items[r]" :key="key">
                <template>
                  <v-list-item-action>
                    <v-checkbox
                      v-model="h"
                      :value="key"
                      @change="k = ''"
                    ></v-checkbox>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title>{{ key }}</v-list-item-title>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </template>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card outlined flat>
            <v-card-title class="text-h5 text-center grey lighten-2">
              所在・函
            </v-card-title>
            <template v-if="h !== ''">
              <v-list-item v-for="(item, key) in items[r][h]" :key="key">
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
  k: string = ''

  items: any = {}

  async mounted() {
    let index: any = await axios.get(process.env.BASE_URL + '/data/tree.json')
    index = index.data
    this.items = index
  }

  search() {
    const query: any = {}

    if (this.r) {
      query['main[refinementList][連]'] = this.r
    }

    if (this.h) {
      query['main[refinementList][箱]'] = this.h
    }

    if (this.k) {
      query['main[refinementList][函册次]'] = this.k
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
