<style>
  iframe{
    border: 0;
    margin: 0;
    padding: 0
  }
</style>

<style>
/* Generic Style */
.markdown {
  line-height: 180% !important;
  font-size: 110% !important;

  --title1Color: darkblue;
  --title2Color: teal;
  --title3Color: darkblue;
  --title3NumberColor: white;
  --title3NumberBG: darkblue;

  --lightShade: rgb(235,237,244);
  --darkShade: rgb(95,172,220);
  --bqText: white;
  --bqBackground: rgb(48,65,147);
}

.markdown img{
  max-width: 100%;
}

/* Titles */
.markdown h1 {
  font-size: 160% !important;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  color: var(--title1Color);
  margin: 40px 0;
}

.markdown h2 {
  font-size: 140% !important;
  letter-spacing: 2px;
  text-align: center;
  color: var(--title2Color);
  margin: 30px 0;
}

.markdown h3 {
  text-transform: uppercase;
  padding: 12px 12px 12px 18px;
  line-height: 100%;
  color: var(--title3Color);
  background-color: var(--lightShade);
}

.markdown h3::first-letter {
  display: inline-block;
  line-height: 100%;
  vertical-align: -10%;
  font-size: 160%;
  border-radius: 100%;
  font-weight: 500;
  color: var(--title3NumberColor);
  background-color: var(--title3NumberBG);
  padding: 0 8px;
  margin-right: 8px;
}

.markdown p{
  margin: 0;
  padding: 15px;
  text-align: justify;
}

.markdown table{
  width: 100%;
  text-align: justify;
}

.markdown table th:empty{
  height: 0px;
  margin: 0px;
  padding: 0px;
}

.markdown table td{
  padding: 12px;
}

.markdown table td:first-child{
  width: 150px;
  text-align: center;
}

.markdown blockquote p{
  background-color: transparent !important;
}


/* Alternating colored tables and Ps */
.markdown table:nth-child(2n+1){
  background-color: var(--lightShade);
}

.markdown p:nth-child(2n+1){
  background-color: var(--lightShade);
}

/* Color of table after blockquote */
.markdown h3 + table, .markdown h3 + p{
  background-color: var(--darkShade) !important;
}

.markdown blockquote{
  color: var(--bqText);
  background-color: var(--bqBackground);
  padding: 20px 30px;
}

</style>

<style>
/* Grid style for tables: '.grid' */

.markdown.grid table td:first-child{
  width: auto;
}

.markdown.grid table{
  border-spacing: 0;
  border-collapse: collapse;

  margin: 0 0 48px 0;
}

.markdown.grid table th{
  color: white;
  background-color: var(--bqBackground);
  border: 1px solid var(--bqBackground);
  padding: 8px;
}

.markdown.grid table td, th{
  /* border-bottom: 1px solid black; */
  padding: 8px 12px;
}

.markdown.grid table tr:nth-child(2n+1){
  background-color: var(--lightShade);
}


</style>

<style>
/* Green theme Style: 'green-theme' */
.markdown.green-theme{
  --lightShade: rgb(236,242,241);
  --darkShade: rgb(198,239,222);
  --bqBackground: rgb(92,146,135);
}
</style>

<style>
/* Green theme Style: 'yellow-theme' */
.markdown.yellow-theme{
  --lightShade: rgb(251,252,238);
  --darkShade: rgb(224,230,108);
}
</style>

<style>
/* Orange theme Style: 'orange-theme' */
.markdown.orange-theme{
  --lightShade: rgb(253,251,235);
  --darkShade: rgb(247,206,168);
  --bqBackground: rgb(240,143,88);
}
</style>

<style>
/* White theme Style: 'white-theme' */
.markdown.white-theme{
  --title3Color: white;
  --title3NumberColor: darkblue;
  --title3NumberBG: white;
  --lightShade: rgb(86,100,166);
  --darkShade: white;
}
</style>


<template>
  <v-card flat>
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
      <v-menu v-if="articlesSameMaster.length > 0" offset-y>
        <v-btn slot="activator" flat>
          {{ article.locale }}
          <v-icon right>
            expand_more
          </v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="a in articlesSameMaster" :key="a.slug" :to="a.link">
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

    <v-layout v-if="isPdf" ma-0>
      <v-flex xs6 pa-1>
        <v-btn block flat outline :disabled="!viewAsPDF" @click="viewAsPDF = false">View as Text</v-btn>
      </v-flex>
      <v-flex xs6 pa-1>
        <v-btn block flat outline :disabled=" viewAsPDF" @click="viewAsPDF = true">View as PDF</v-btn>
      </v-flex>
    </v-layout>
    
    <!-- Article Content as TEXT -->
    <v-card-text v-if="!viewAsPDF" :dir="localeDir" :class="['markdown', article.extra_style]">
      <vue-markdown>{{ article.body }}</vue-markdown>
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

    <!-- Article Content as PDF -->
    <v-sheet v-else>
      <iframe :src="pdfURL + '#toolbar=0'" width="100%" height="800px" />
    </v-sheet>

    <!-- Attachments -->
    <v-card-text>
      <v-sheet class="grey lighten-4 pa-3">
        <h2 class="mb-2">{{ $t('noums.files') }}</h2>
        <!-- List of attachments -->
        <AttachmentList :attachments="article.attachments" @change="reloadContent" />
        <!-- Upload form for editor -->
        <template v-if="currentUser.is_editor">
          <br>
          <br>
          <h3 mb-2>{{ $t('components.Attachment.upload') }}</h3>
          <AttachmentUpload model="content" :object-id="article.id" @upload="reloadContent" />
        </template>
      </v-sheet>
    </v-card-text>

  </v-card>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n";
import AttachmentUpload from "@/components/input/AttachmentUpload";
import AttachmentList from "@/components/attachment/AttachmentList";

export default {

  components:{
    AttachmentUpload,
    AttachmentList
  },
  props : ["article", "articlesSameMaster"],

  data(){
    return {
      moment,
      getFlagIso,
      viewAsPDF: false
    }
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
    isPdf(){
      if(!this.article.attachments || this.article.attachments.length == 0)
        return false;
      return this.article.attachments[0].mime_type == 'application/pdf';
    },
    pdfURL(){
      return this.article.attachments[0].url;
    },
    isSmallScreen(){
      return document.body.clientWidth < 950;
    },
    localeDir(){
      if (this.article.locale == 'ar') return 'rtl';
      return 'ltr';
    }
  },

  created() {    
    if(this.isPdf && !this.isSmallScreen){
      this.viewAsPDF = true;
    }
  },

  methods: {
    async reloadContent(){
      console.log("Reloading article")
      this.$store.dispatch('content/load', [this.article.slug])
    }
  },

}
</script>
