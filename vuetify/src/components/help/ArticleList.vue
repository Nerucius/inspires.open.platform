<style scoped>
    .flag-icon{
        width: 24px; height:22px; display:inline-block
    }
    .topic-tag{
      position: absolute;
      font-size: 70%;
      font-weight: 700;
      top: 2px;
      right: 4px
    }
</style>

<template>
  <div>
    <v-list two-line>
      <template v-for="(group, i) in groupedArticles">
        <v-divider v-if="i > 0" :key="group.master_id + '-sep'" />

        <v-list-tile :key="group.master_id" :to="group.article.link">
          <v-flex shrink mr-5 class="hidden-xs-only text-xs-center">
            <v-icon>mdi-school</v-icon><br>
            <small class="text-uppercase"><strong>{{ group.article.topic }}</strong></small>
          </v-flex>
          <!-- <v-list-tile-avatar>
            <v-icon>mdi-book</v-icon>
          </v-list-tile-avatar> -->

          <v-list-tile-content>
            <div class="hidden-sm-and-up text-uppercase topic-tag">
              {{ group.article.topic }}
            </div>
            <v-list-tile-title>
              <strong>
                {{ group.article.title }}
              </strong>
            </v-list-tile-title>
            <v-list-tile-sub-title>
              {{ group.article.summary }}
            </v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action v-if="flags" class="hidden-sm-and-down">
            <!-- Flags for all available translated languages -->
            <v-layout row wrap style="max-width:Calc(32px*4)">
              <v-flex v-for="flag in group.flags.sort()" :key="flag" shrink pa-1 class="text-xs-center">
                <flag
                  :iso="getFlagIso(flag)"
                  :squared="false"
                />
              </v-flex>
            </v-layout>
          </v-list-tile-action>
        </v-list-tile>
      </template>
    </v-list>
  </div>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n"

const unique = (value, index, self) => {
  return self.indexOf(value) === index
}

export default {
    props: ['articles', 'flags'],

    data() {
        return {
            getFlagIso
        }
    },

    computed: {

      groupedArticles(){
        let userLang = this.$store.getters['preferences/lang'];
        let masters = this.articles.map(a => a.master).filter(unique).sort();

        let grouped = masters.map(m => {
          let masterArticles = this.articles.filter(a => a.master == m)

          let flags = masterArticles.map(a => a.locale)
          let userArticle
          try {
            userArticle = masterArticles.filter(a => a.locale == userLang)[0]
          } catch (error) {
            userArticle = masterArticles.filter(a => a.locale == 'en')[0]
          }

          return {
            master_id: m,
            article: userArticle || masterArticles[0],
            flags: flags
          }
        })

        return grouped
      }
    },
}
</script>