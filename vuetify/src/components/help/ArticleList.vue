<style scoped>
    .flag-icon{
        height: 80%;
    }
</style>

<template>
  <v-list two-line>
    <template v-for="(article, i) in articles">
      <v-divider v-if="i > 0" :key="article.slug + '-sep'" />

      <v-list-tile :key="article.slug" :to="article.link">
        <v-flex shrink mr-5 class="text-xs-center">
          <v-icon>mdi-school</v-icon><br>
          <small class="text-uppercase"><strong>{{ article.topic }}</strong></small>
        </v-flex>
        <!-- <v-list-tile-avatar>
          <v-icon>mdi-book</v-icon>
        </v-list-tile-avatar> -->

        <v-list-tile-content>
          <v-list-tile-title>
            <strong>
              {{ article.title }}
            </strong>
          </v-list-tile-title>
          <v-list-tile-sub-title>
            {{ article.summary }}
          </v-list-tile-sub-title>
        </v-list-tile-content>
        <v-list-tile-action>
          <flag v-if="flags"
                :iso="getFlagIso(article.locale)"
                :squared="false"
                style="width: 40px; height:100%"
          />
        </v-list-tile-action>
      </v-list-tile>
    </template>
  </v-list>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n"

export default {
    props: ['articles', 'flags'],

    data() {
        return {
            getFlagIso
        }
    },
}
</script>