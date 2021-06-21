<template>
  <div>
    <v-sheet color="grey lighten-2" class="pa-5 mb-4">
      <h1 class="text-center my-10">
        <img class="mr-2" width="90" :src="baseUrl + '/img/「猶龍窟」印.png'" />
        酉蓮社(旧増上寺報恩蔵)蔵嘉興版大蔵経目録データベース
      </h1>
    </v-sheet>
    <v-container>
      <v-row>
        <v-col cols="12" :sm="12">
          <v-sheet color="grey lighten-2" class="pa-5 mb-4">
            <div>
              切り替え
              <ul>
                <li>
                  <nuxt-link
                    :to="
                      localePath({
                        name: 'search',
                      })
                    "
                    >書名目録</nuxt-link
                  >
                </li>
                <li>
                  <nuxt-link
                    :to="
                      localePath({
                        name: 'advanced',
                      })
                    "
                    >詳細目録</nuxt-link
                  >
                </li>
              </ul>
            </div>
            <!--
            <div class="mt-4">
              IIIF画像
              <ul>
                <li>
                  <a
                    target="_blank"
                    :href="
                      'https://www.kanzaki.com/works/2016/pub/image-annotator?u=' +
                      uRenja
                    "
                    >酉蓮社本</a
                  >
                </li>
                <li>
                  <a
                    target="_blank"
                    :href="
                      'https://www.kanzaki.com/works/2016/pub/image-annotator?u=' +
                      kando
                    "
                    >『大正新脩大蔵経勘同目録』</a
                  >
                </li>
              </ul>
            </div>
            <div class="mt-4">
              データ
              <ul>
                <li>
                  <a target="_blank" :href="metadata">Excel</a>
                </li>
              </ul>
            </div>
            -->
          </v-sheet>
          <p>
            <a :href="baseUrl + '/はじめに・凡例.pdf'">はじめに・凡例</a>
          </p>
          <p>
            <a :href="baseUrl + '/現在の酉蓮社における収蔵状況.pdf'"
              >現在の酉蓮社における収蔵状況</a
            >
          </p>
          <p>
            <a href="https://taishozo.github.io/db/"
              >『大正新脩大蔵経』底本・校本DB</a
            >
          </p>
          <p>
            <nuxt-link :to="localePath({ name: 'dataset' })"
              >データセット</nuxt-link
            >
          </p>
          <v-tooltip top>
            <template v-slot:activator="{ on }">
              <v-img
                max-height="600px"
                :src="baseUrl + '/img/経箱画像.png'"
                contain
                v-on="on"
              />
            </template>
            <span>酉蓮社本を収める経箱 1 箱に 3 函を納める</span>
          </v-tooltip>
        </v-col>
        <v-col v-if="false" cols="12" :sm="9">
          <v-card outlined>
            <v-container><h2 class="text-center">所在</h2></v-container>
          </v-card>

          <v-row class="my-5">
            <v-col>
              <v-card outlined>
                <v-container
                  ><h3 class="text-center">所在：連</h3>
                  <v-list dense>
                    <div style="max-height: 800px;" class="overflow-y-auto">
                      <template v-for="(value, index) in 7">
                        <v-list-item :key="'bucket_' + index">
                          <v-list-item-content
                            class="my-0 py-0"
                            style="word-break: break-word;"
                          >
                            <v-checkbox
                              v-model="rens"
                              class="mb-0 mt-1 ml-1 py-0"
                              align="center"
                              dense
                              x-small
                              color="primary"
                              :label="value"
                              :value="value"
                            ></v-checkbox>
                          </v-list-item-content>
                        </v-list-item>
                        <v-divider :key="`divider-${index}`"></v-divider>
                      </template>
                    </div>
                  </v-list>
                </v-container>
              </v-card>
            </v-col>
            <v-col>
              <v-card outlined>
                <v-container
                  ><h3 class="text-center">所在：箱</h3>
                  <v-list dense>
                    <div style="max-height: 800px;" class="overflow-y-auto">
                      <template v-for="(value, index) in 111">
                        <v-list-item :key="'bucket_' + index">
                          <v-list-item-content
                            class="my-0 py-0"
                            style="word-break: break-word;"
                          >
                            <v-checkbox
                              v-model="hakos"
                              class="mb-0 mt-1 ml-1 py-0"
                              align="center"
                              dense
                              x-small
                              color="primary"
                              :label="value"
                              :value="value"
                            ></v-checkbox>
                          </v-list-item-content>
                        </v-list-item>
                        <v-divider :key="`divider-${index}`"></v-divider>
                      </template>
                    </div>
                  </v-list>
                </v-container> </v-card
            ></v-col>
            <v-col>
              <v-card outlined>
                <v-container
                  ><h3 class="text-center">所在：函</h3>
                  <v-list dense>
                    <div style="max-height: 800px;" class="overflow-y-auto">
                      <template v-for="(value, index) in 333">
                        <v-list-item :key="'bucket_' + index">
                          <v-list-item-content
                            class="my-0 py-0"
                            style="word-break: break-word;"
                          >
                            <v-checkbox
                              v-model="kans"
                              class="mb-0 mt-1 ml-1 py-0"
                              align="center"
                              dense
                              x-small
                              color="primary"
                              :label="value"
                              :value="value"
                            ></v-checkbox>
                          </v-list-item-content>
                        </v-list-item>
                        <v-divider :key="`divider-${index}`"></v-divider>
                      </template>
                    </div>
                  </v-list>
                </v-container> </v-card
            ></v-col>
          </v-row>
          全体の収蔵状況は<a
            :href="baseUrl + '/現在の酉蓮社における収蔵状況.pdf'"
            >「現在の酉蓮社における収蔵状況」</a
          >をご覧ください。
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class Page extends Vue {
  head() {
    return {
      titleTemplate: null,
    }
  }

  slides: string[] = [process.env.BASE_URL + '/img/経箱画像.png']

  baseUrl: string = process.env.BASE_URL || ''

  image: string = this.$store.state.thumbnail ? this.$store.state.thumbnail : ''

  uRenja: any = this.baseUrl + '/iiif2/collection/top.json'
  metadata: any = this.baseUrl + '/metadata/data.xlsx'
  kando: any = process.env.db + '/iiif/kandomokuroku/manifest.json'

  get title(): string {
    return this.$store.state.title
  }

  get thumbnail(): string {
    return this.$store.state.thumbnail
  }

  get attribution(): string {
    return this.$store.state.attribution
  }

  get description(): string {
    return this.$store.state.description
  }

  rens: number[] = []

  /*
  async fetch(context: any) {
    const store = context.store

    const uri = process.env.BASE_URL + '/iiif/collection/advanced.json'
    const index = await context.app.$searchUtils.createIndex(uri)
    context.app.$searchUtils.initStore(store, index)

    const result = context.app.$searchUtils.search(
      store.state.index,
      store.state.data,
      store.state.query
    )

    context.store.commit('setResult', result)
  }
  */
}
</script>
