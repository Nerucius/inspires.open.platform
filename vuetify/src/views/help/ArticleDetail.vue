<template>
  <v-layout row wrap align-content-start justify-center>

    <!-- Title and header -->
    <v-flex xs12 xl8>
      <v-layout row wrap justify-end pa-2>
        <v-flex grow pa-0 pl-1>
          <h1>{{ $t("pages.help.title") }}</h1>
        </v-flex>
        <!-- Editor Controls -->
        <template v-if="currentUser.is_editor">
          <v-flex shrink pa-0>
            <v-btn outline color="warning" :href="editContentURL" target="_blank">
              <v-icon left>edit</v-icon> Edit This content
            </v-btn>
          </v-flex>
        </template>
      </v-layout>
    </v-flex>

    <!-- Content of the Article -->
    <v-flex v-if="!!article" xs12 xl8>
      <ArticleContent :key="article.id" :article="article" :articles-same-master="articles" />
    </v-flex>

    <!-- Attached Materials -->
    <v-flex xs12 xl8>
      <AttachmentMenu :expanded="article.attachments.length > 0" :content="article" @change="loadContent" />
    </v-flex>

    <!-- Feedback form -->
    <v-flex xs12 xl8>
      <FeedbackForm :title="article.title" feedback-type="ARTICLE_FEEDBACK" model="content" :object-id="article.id" />
    </v-flex>


  </v-layout>
</template>

<script>
import ArticleContent from "@/components/help/ArticleContent";
import AttachmentMenu from "@/components/attachment/AttachmentMenu";
import FeedbackForm from "@/components/input/FeedbackForm";

import { getFlagIso } from "@/plugins/i18n";
import { API_SERVER } from "@/plugins/resource";

export default {
  metaInfo() {
    return { title: this.article.title }
  },

  components: {
    ArticleContent,
    AttachmentMenu,
    FeedbackForm,
  },

  data() {
    return {
      articles: [],
      getFlagIso,
    }
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
    articleSlug() {
      return this.$route.params.page;
    },
    createContentURL(){
      return API_SERVER + '/admin/backend/content/'
    },
    editContentURL(){
      if(!this.article) return ''
      return API_SERVER + '/admin/backend/content/' + this.article.id + '/change/'
    },
    article(){
      return this.$store.getters["content/detail"](this.articleSlug);
    },
  },

  async created(){
    this.$store.dispatch("content/clear")
    await this.loadContent()

    this.loadRelatedArticles()
  },

  methods:{
    async loadRelatedArticles() {
      await this.$store.dispatch("content/load", {params:{master:this.article.master}});
      this.articles = this.$store.getters["content/all"];
    },

    async loadContent() {
      // load current article
      try {
        await this.$store.dispatch("content/load", [this.articleSlug]);
      } catch (error) {
          this.$router.push({ name: 'help' });
          this.$store.dispatch('toast/warning', this.$t('pages.help.articleDoesNotExist'))
      }
    },
  }
}
</script>

