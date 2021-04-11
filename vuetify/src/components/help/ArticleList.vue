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

<style>
  .v-list--two-line .v-list__tile{
    height: auto !important;
    min-height: 72px;
  }
</style>

<template>
  <div>
    <v-list two-line>
      <template v-for="group in groupedArticles">
        <h2 v-if="group.header" :key="group.master_id + '-header'" class="hidden-xs-only">
          <small class="text-uppercase"><strong>{{ group.article.topic }}</strong></small>
        </h2>

        <v-divider v-if="!group.header" :key="group.master_id + '-sep'" />

        <v-list-tile :key="group.master_id">
          <!-- <v-flex xs2 xl1 mr-4 class="hidden-xs-only text-xs-center">
            <v-icon>mdi-school</v-icon><br>
            <small class="text-uppercase"><strong>{{ group.article.topic }}</strong></small>
          </v-flex> -->
          <v-list-tile-avatar>
            <v-icon>mdi-school</v-icon>
          </v-list-tile-avatar>

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
            <v-layout ml-2 row wrap style="max-width:Calc(34px*5); margin: 0px -12px">
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

        <div v-if="group.spaceAfter" :key="group.master_id + '-spacer'" class="mb-4" />
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

        // Quick exit while loading
        if(masters.length == 0) return [];

        let grouped = masters.map(m => {
          // Articles from the same master, sorted by locale
          let masterArticles = this.articles.filter(a => a.master == m).sort((a,b) => a.locale.localeCompare(b.locale))

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

        // Dividers on topic change and Topic Headers
        grouped[0].header = true
        for(let i = 0; i < grouped.length-1; i++){
          if(grouped[i].article.topic != grouped[i+1].article.topic){
            grouped[i].spaceAfter = true;
            grouped[i+1].header = true;
          }
        }

        return grouped
      }
    },
}
</script>
