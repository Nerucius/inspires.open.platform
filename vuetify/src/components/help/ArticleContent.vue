<style>
  iframe{
    border: 0;
    margin: 0;
    padding: 0
  }
</style>

<style>
.markdown {
  line-height: 180% !important;
}

.markdown h1 {
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  color: darkblue;
  margin: 40px 0;
}

.markdown h2 {
  letter-spacing: 2px;
  text-align: center;
  color: teal;
  margin: 30px 0;
}

.markdown p{
  margin: 0;
  padding: 15px;
  text-align: justify;
}

/* Alternating colored Ps */
.markdown p:nth-child(2n+1){
  background-color: rgb(235,237,244);
}

.markdown table{
  width: 100%;
}

/* Alternating colored Ps */
.markdown table:nth-child(2n+1){
  background-color: rgb(235,237,244);
}

.markdown blockquote{
  background-color: rgb(48,65,147);
  padding: 20px 30px;
  color: white
}
.markdown blockquote p{
  background-color: transparent !important;
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
      <v-menu offset-y v-if="articlesSameMaster.length > 0">
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

    <v-layout ma-0 v-if="isPdf">
      <v-flex xs6 pa-1>
        <v-btn block flat outline :disabled="!viewAsPDF" @click="viewAsPDF = false">View as Text</v-btn>
      </v-flex>
      <v-flex xs6 pa-1>
        <v-btn block flat outline :disabled=" viewAsPDF" @click="viewAsPDF = true">View as PDF</v-btn>
      </v-flex>
    </v-layout>
    
    <!-- Article Content as TEXT -->
    <v-card-text class="markdown" v-if="!viewAsPDF">
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
      <iframe :src="pdfURL + '#toolbar=0'" width="100%" height="800px"></iframe>
    </v-sheet>

    <!-- Attachments -->
    <v-card-text>
      <v-sheet class="grey lighten-4 pa-3">
        <h2 class="mb-2">{{ $t('noums.attachments') }}</h2>
        <!-- List of attachments -->
        <AttachmentList :attachments="article.attachments" />
        <!-- Upload form for admins -->
        <template v-if="currentUser.is_administrator">
          <br />
          <br />
          <h3 mb-2>Upload Attachment</h3>
          <AttachmentUpload model='content' :objectId='article.id' @upload="reloadArticle"/>
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
  props : ["article", "articlesSameMaster"],

  components:{
    AttachmentUpload,
    AttachmentList
  },

  data(){
    return {
      moment,
      getFlagIso,
      viewAsPDF: false
    }
  },

  created() {    
    if(this.isPdf && !this.isSmallScreen){
      this.viewAsPDF = true;
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
    }
  },

  methods: {
    async reloadArticle(){
      console.log("Reloading article")
      this.$store.dispatch('content/load', [this.article.slug])
    }
  },

}
</script>

<style>

</style>
