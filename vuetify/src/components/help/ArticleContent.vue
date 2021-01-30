<template>
  <v-card v-if="article != null" flat>
    <!-- Toolbar -->
    <v-toolbar dense flat dark color="grey darken-3">
      <v-toolbar-title>
        <span class="grey--text">
          {{ article.topic }} |
        </span>{{ article.title }}
      </v-toolbar-title>
      <v-spacer />
      <!-- Back button -->
      <v-btn flat exact :to="{ name: 'help' }">
        <v-icon left>
          mdi-arrow-left
        </v-icon>{{ $t("actions.back") }}
      </v-btn>

      <!-- This article in other languages -->
      <v-menu offset-y v-if="articlesSameMaster.length > 0">
        <v-btn slot="activator" flat>
          {{ article.locale }}
          <v-icon right>
            expand_more
          </v-icon>
        </v-btn>
        <v-list>
          <v-list-tile
            v-for="a in articlesSameMaster"
            :key="a.slug"
            :to="a.link"
          >
            <v-list-tile-title>
              <small>{{ a.locale | uppercase }}</small>
            </v-list-tile-title>

            <flag
              :iso="getFlagIso(a.locale)"
              :squared="false"
              style="width: 40px"
            />
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>

    <!-- Article Content -->
    <v-card-text class="markdown" v-if="!isPdf">
      <vue-markdown v-if="article != null">{{ article.body }}</vue-markdown>
      <v-layout mt-3 justify-end>
        <v-flex shrink class="grey--text">
          <span :title="moment(article.modified_at).format('L LT')">
            {{
              $t("misc.lastUpdated", {
                time: moment(article.modified_at).fromNow(),
              })
            }}
          </span>
        </v-flex>
      </v-layout>
    </v-card-text>

    <v-sheet v-else>
      <br>
      <iframe
        :src="pdfURL + '#toolbar=0'" width="100%" height="800px">
      </iframe>
    </v-sheet>

    <!-- Attachments -->
    <v-card-text>
      <v-sheet class="grey lighten-4 pa-3">
        <h2 class="mb-2">{{ $t('noums.attachments') }}</h2>
        <v-list>
          <v-list-tile v-for="att in article.attachments" :key="att.id" :to="att.url">
            <v-list-tile-action>
              <v-icon>mdi-file</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              {{ att.name }}
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n";

export default {
  props : ["article", "articlesSameMaster"],

  data(){
    return {
      moment,
      getFlagIso
    }
  },

  computed:{
    isPdf(){
      if(!this.article.attachments || this.article.attachments.length == 0)
        return false;
      return this.article.attachments[0].mime_type == 'application/pdf';
    },
    pdfURL(){
      return this.article.attachments[0].url;
    }
  }

}
</script>

<style>

</style>
