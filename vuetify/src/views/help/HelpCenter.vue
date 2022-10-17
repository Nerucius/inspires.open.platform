<template>
  <v-layout row wrap align-content-start justify-center>
    <!-- Title bar -->
    <v-flex xs12 xl8>
      <v-layout row wrap justify-end pa-2>
        <v-flex grow pa-0 pl-1>
          <h1>{{ $t("pages.help.title") }}</h1>
        </v-flex>
        <!-- Admin Controls -->
        <template v-if="currentUser.is_editor">
          <v-flex shrink pa-0>
            <v-btn outline color="success" :href="createContentURL" target="_blank">
              <v-icon left>add</v-icon> Create New Content
            </v-btn>
          </v-flex>
        </template>
      </v-layout>
    </v-flex>

    <!-- Courses List section-->
    <v-flex xs12 xl8 mb-4>
      <CourseList :courses="courses" :flags="true" />
    </v-flex>

    <!-- Article List Section -->
    <v-flex xs12 xl8>
      <v-card flat class="pb-3">
        <v-toolbar dense flat dark color="grey darken-3">
          <v-toolbar-title>{{ $t("pages.help.allArticles") }}</v-toolbar-title>
        </v-toolbar>

        <v-card-text>
          <v-layout justify-center>
            <v-flex xs12 sm9 md9 lg6>
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
import CourseList from "@/components/help/CourseList";
import { getFlagIso } from "@/plugins/i18n";
import { API_SERVER } from "@/plugins/resource";

const unique = (value, index, self) => {
  return self.indexOf(value) === index
}

export default {
  metaInfo() {
    return { title: this.$t("pages.help.title") }
  },

  components: {
    ArticleList,
    CourseList,
  },

  data() {
    return {
      getFlagIso,
      searchTerm: '',
      filterTopic: '',
      contents: [],
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
    topics(){
      return this.articles.map(a => a.topic).filter(unique)
    },
    articles(){
      return this.contents.filter(c => c.type == 'HELP')
    },
    courses(){
      return this.contents.filter(c => c.type == 'COURSE')
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
    await Promise.all([this.loadContents()])

    // let listener = this.$store.subscribe((mutation, _) => {
    //   // Listen to Language changes to refresh article list
    //   if (mutation.type == "preferences/SET_PREFERENCE") this.loadContents();
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

  methods: {
    async loadContents() {
      this.$store.dispatch("content/clear");

      await this.$store.dispatch("content/load");
      this.contents = this.$store.getters["content/all"];
    },
  },
};
</script>
