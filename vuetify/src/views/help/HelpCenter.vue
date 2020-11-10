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
      <h1>{{ $t("pages.help.title") }}</h1>
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

    <v-flex xs12>
      <!-- Article Page -->
      <v-card v-if="article != null" flat>
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
          <v-menu offset-y>
            <v-btn slot="activator" flat>
              {{ article.locale }}
              <v-icon right>
                expand_more
              </v-icon>
            </v-btn>
            <v-list>
              <v-list-tile
                v-for="a in articlesSameMaster(article.master)"
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

        <v-card-text class="markdown">
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
      </v-card>

      <!-- Article List Page -->
      <v-card v-else flat class="pb-3">
        <v-toolbar dense flat dark color="grey darken-3">
          <v-toolbar-title>{{ $t("pages.help.allArticles") }}</v-toolbar-title>
        </v-toolbar>

        <v-card-text>
          <ArticleList :articles="articlesSameLanguage" />
          <hr class="mt-3 mb-1">
        </v-card-text>

        <v-expansion-panel class="elevation-0">
          <v-expansion-panel-content>
            <template v-slot:header>
              <h3>{{ $t('pages.help.articlesOtherLanguages') }}</h3>
            </template>
            <v-card-text>
              <ArticleList :articles="articlesDiffLanguage" :flags="true" />
            </v-card-text>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import ArticleList from "@/components/help/ArticleList";
import { getFlagIso } from "@/plugins/i18n";

export default {
  metaInfo() {
    return {
      title: this.$t("pages.helpCenter.title"),
    };
  },

  components: {
    ArticleList,
  },

  data() {
    return {
      getFlagIso,
      moment,
      article: null,
      articles: [],
      onDestroy: [],
    };
  },

  computed: {
    currentLang() {
      return this.$store.getters["preferences/lang"];
    },
    articleSlug() {
      return this.$route.params.page;
    },
    articlesSameLanguage() {
      return this.articles.filter((a) => a.locale == this.currentLang);
    },
    articlesDiffLanguage() {
      return this.articles.filter((a) => a.locale != this.currentLang).sort((a,b) => b.master-a.master);
    },
  },

  async created() {
    this.loadArticles();
    this.loadArticleDetail();

    let unsub = this.$store.subscribe((mutation, _) => {
      // Listen to Language changes to refresh article list
      if (mutation.type == "preferences/SET_PREFERENCE") this.loadArticles();
    });
    this.onDestroy = this.onDestroy.concat(unsub);
  },

  destroyed() {
    // cancel all subs
    this.onDestroy.forEach((f) => f());
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
      this.article = this.$store.getters["content/detail"](this.articleSlug);

      // filter article list for this master
      // await this.$store.dispatch("content/load", {params: {master: this.article.master}});
      // this.articles = this.$store.getters["content/all"];
    },

    articlesSameMaster(masterId) {
      return this.articles.filter((a) => a.master == masterId);
    },
  },
};
</script>
