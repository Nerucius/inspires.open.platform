<style>
  .markdown {
    line-height: 250%;
  }

  .markdown h1 {
    font-size: 1.5em;
  }
  .markdown h2 {
    font-size: 1.3em;
  }
  .markdown h3 {
    font-size: 1.1em;
  }
</style>

<template>
  <v-layout row wrap align-content-start>
    <!-- Title bar -->
    <v-flex xs12>
      <v-layout row wrap justify-end pa-2>
        <v-flex grow pa-0 pl-1>
          <h1>{{ $t("pages.help.title") }}</h1>
        </v-flex>
        <!-- Admin Controls -->
        <template v-if="currentUser.is_administrator">
          <v-flex shrink pa-0>
            <v-btn outline color="success" :href="createContentURL" target="_blank">Create New Content</v-btn>
          </v-flex>
          <v-flex v-if="isArticleDetail" shrink pa-0>
            <v-btn outline color="warning" :href="editContentURL" target="_blank">Edit This content</v-btn>
          </v-flex>
        </template>
      </v-layout>
    </v-flex>

    <!-- Article Page -->
    <v-flex v-if="isArticleDetail && !!article" xs12>
      <ArticleContent :key="article.id" :article="article" :articles-same-master="articlesSameMaster(article.master)" />
    </v-flex>

    <!-- Article List Page -->
    <v-flex v-else xs12>
      <v-card flat class="pb-3">
        <v-toolbar dense flat dark color="grey darken-3">
          <v-toolbar-title>{{ $t("pages.help.allArticles") }}</v-toolbar-title>
        </v-toolbar>

        <v-card-text>
          <v-layout justify-center>
            <v-flex xs12 sm9 md6>
              <v-text-field
                v-model="searchTerm"
                outline
                class="my-3"
                hide-details
                single-line
                prepend-icon="search"
                browser-autocomplete="off"
                :placeholder="$t('actions.search')"
              />
            </v-flex>
          </v-layout>

          <!-- TODO: Filter by Topic -->
          <!-- <v-layout mb-3 wrap>
            <v-flex pa-0 ma-0 shrink v-for="topic in topics" :key="topic">
              <v-btn @click="filterTopic = topic" :disabled="topic==filterTopic">{{ topic }}</v-btn>
            </v-flex>
          </v-layout> -->

          <ArticleList :articles="articleSearch" :flags="true" />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import ArticleList from "@/components/help/ArticleList";
import ArticleContent from "@/components/help/ArticleContent";
import { getFlagIso } from "@/plugins/i18n";
import { API_SERVER } from "@/plugins/resource";

const unique = (value, index, self) => {
  return self.indexOf(value) === index
}

export default {
  metaInfo() {
    var title;
    if(!this.isArticleDetail)
      title = this.$t("pages.help.title")
    else
      title = this.article.title
    return {title }
  },

  components: {
    ArticleList,
    ArticleContent,
  },

  data() {
    return {
      getFlagIso,
      moment,
      searchTerm: '',
      filterTopic: '',
      articles: [],
      onDestroy: [],
    };
  },

  computed: {
    currentUser(){
      return this.$store.getters['user/current']
    },
    currentLang() {
      return this.$store.getters["preferences/lang"];
    },
    createContentURL(){
      return API_SERVER + '/admin/backend/content/'
    },
    editContentURL(){
      if(!this.article) return ''
      return API_SERVER + '/admin/backend/content/' + this.article.id + '/change/'
    },
    isArticleDetail(){
      return !!this.$route.params.page
    },
    articleSlug() {
      return this.$route.params.page;
    },
    topics(){
      return this.articles.map(a => a.topic).filter(unique)
    },
    article(){
      if(this.articleSlug)
        return this.$store.getters["content/detail"](this.articleSlug);
      return null;
    },
    articleSearch(){
      let articles = this.articles;

      if(this.filterTopic){
        articles = articles.filter(a => a.topic == this.filterTopic);
      }

      if(!this.searchTerm) return articles;
      let l = s => s.toLowerCase()
      let s = l(this.searchTerm)

      return this.articles.filter(a => {
        if (l(a.topic).indexOf(s) >= 0) return true
        if (l(a.title).indexOf(s) >= 0) return true
        if (l(a.summary).indexOf(s) >= 0) return true
        return false
      })
    }
  },

  async created() {
    await Promise.all([this.loadArticles(), this.loadArticleDetail()])

    // let listener = this.$store.subscribe((mutation, _) => {
    //   // Listen to Language changes to refresh article list
    //   if (mutation.type == "preferences/SET_PREFERENCE") this.loadArticles();
    // });
    // this.onDestroy = [...this.onDestroy, listener]

    this.$nextTick(() => {
      if (!!this.$route.query.q){
        this.searchTerm = this.$route.query.q
      }

      if(!!this.$route.query.master){
        let master = this.$route.query.master
        let locale = this.$i18n.locale

        // Try to match article by master and locale
        let masterArticle = this.articles.filter(a => a.master == master && a.locale == locale)
        if(masterArticle.length == 0)
          masterArticle = this.articles.filter(a => a.master == master && a.locale == 'en')
        
        // If we found one, redirect
        if(masterArticle.length != 0){
          let goToArticle = masterArticle[0]
          this.$router.push(goToArticle.link)
        }
      }
    })
  },

  destroyed() {
    // cancel all subs
    this.onDestroy.forEach((f) => f());
    this.onDestroy = []
  },

  methods: {
    async loadArticles() {
      this.$store.dispatch("content/clear");

      // Loading userlang?
      // let userLang = this.currentLang;
      // await this.$store.dispatch("content/load", { params : {locale: userLang} });
      
      await this.$store.dispatch("content/load", {params:{master__type:"HELP"}});
      this.articles = this.$store.getters["content/all"];
    },

    async loadArticleDetail() {
      if (!this.articleSlug) return;

      // load current article
      this.$store.dispatch("content/clear");
      try {
        await this.$store.dispatch("content/load", [this.articleSlug]);
      } catch (error) {
          this.$router.push({ name: 'help' });
          this.$store.dispatch('toast/warning', this.$t('pages.help.articleDoesNotExist'))
      }
    },

    articlesSameMaster(masterId) {
      return this.articles.filter((a) => a.master == masterId);
    },
  },
};
</script>
