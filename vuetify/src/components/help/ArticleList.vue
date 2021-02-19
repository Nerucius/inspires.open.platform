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
    .v-list a{
    text-decoration: none;
    color:inherit;
  }
</style>

<template>
  <div>
    <v-list two-line>
      <template v-for="group in groupedArticles">
        <v-divider :key="group.master_id + '-sep'" />

        <v-list-tile :key="group.master_id">
          <v-flex xs2 xl1 mr-5 class="hidden-xs-only text-xs-center">
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
                <router-link :to="group.article.link">
                  {{ group.article.title }}
                </router-link>
              </strong>
            </v-list-tile-title>
            <v-list-tile-sub-title>
              {{ group.article.summary }}
            </v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action v-if="flags" class="hidden-sm-and-down">
            <!-- Flag links for all available translated languages -->
            <v-layout row wrap style="max-width:Calc(32px*4)">
              <v-flex v-for="other in group.others.sort()" :key="other.id" shrink pa-1 class="text-xs-center">
                <router-link :to="other.link">
                  <flag
                    :iso="getFlagIso(other.locale)"
                    :squared="false"
                  />
                </router-link>
              </v-flex>
            </v-layout>
          </v-list-tile-action>
        </v-list-tile>

        <v-divider v-if="group.spaceAfter" :key="group.master_id + '-spacer'" class="mb-4" />
      </template>
      <v-divider />
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

          let userArticle
          // Decide the article we show to the user, if we can match the user's language, shwo that one, otherwise, find the english one.
          try {
            userArticle = masterArticles.filter(a => a.locale == userLang)[0]
          } catch (error) {
            userArticle = masterArticles.filter(a => a.locale == 'en')[0]
          }

          return {
            master_id: m,
            article: userArticle || masterArticles[0],
            others: masterArticles
          }
        })

        // Sort by master-inheritet property `sorting`
        grouped.sort((a,b) => a.article.sorting - b.article.sorting )

        // Dividers on topic change
        for(let i = 0; i < grouped.length-1; i++){
          if(grouped[i].article.topic != grouped[i+1].article.topic)
            grouped[i].spaceAfter = true;
        }

        return grouped
      }
    },
}
</script>
