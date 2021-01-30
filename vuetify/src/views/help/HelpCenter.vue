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

    <!-- <v-flex md4 hidden-sm-and-down>
      <v-card flat>
        <v-card-title>
          <h2>About the Help Center</h2>
        </v-card-title>
        <v-card-text>

        </v-card-text>
      </v-card>
    </v-flex> -->

    <v-flex v-if="isArticleDetail && !!article" xs12>
      <!-- Article Page -->
      <ArticleContent :key="article.id" :article="article" :articlesSameMaster="articlesSameMaster(article.master)" />
    </v-flex>

    <v-flex v-else xs12>
      <!-- Article List Page -->
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

export default {
  metaInfo() {
    return {
      title: this.$t("pages.help.title"),
    };
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
    article(){
      if(this.articleSlug)
        return this.$store.getters["content/detail"](this.articleSlug);
      return null;
    },
    articleSearch(){
      if(!this.searchTerm) return this.articles;
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

    let listener = this.$store.subscribe((mutation, _) => {
      // Listen to Language changes to refresh article list
      if (mutation.type == "preferences/SET_PREFERENCE") this.loadArticles();
    });

    this.onDestroy = [...this.onDestroy, listener]

    this.$nextTick(() => {
      if (!!this.$route.query.q){
        this.searchTerm = this.$route.query.q
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
      let userLang = this.currentLang;

      this.$store.dispatch("content/clear");
      await this.$store.dispatch("content/load", {params:{master__type:"HELP"}});
      // await this.$store.dispatch("content/load", { params : {locale: userLang} });
      this.articles = this.$store.getters["content/all"];
    },

    async loadArticleDetail() {
      if (!this.articleSlug) return;

      // load current article
      this.$store.dispatch("content/clear");
      await this.$store.dispatch("content/load", [this.articleSlug]);
    },

    articlesSameMaster(masterId) {
      return this.articles.filter((a) => a.master == masterId);
    },
  },
};
</script>
