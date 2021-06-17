<style scoped>
  .cover-image{
    width: 100%;
    position: absolute;
    top: -64px;
  }

  .module-header .v-card__text{
    font-size: 120%;
    line-height: 180%;
  }
</style>

<template>
  <v-layout row wrap align-content-start justify-center>

    <v-parallax
      v-if="isModule"
      class="cover-image"
      height="800"
      :src="content.image_url"
    />

    <!-- Navigation Buttons -->
    <v-layout justify-end>
      <v-flex v-if="currentUser.is_editor" shrink>
        <v-btn v-if="!isModule" color="success" :href="createModuleURL" target="_blank">
          <v-icon left>add</v-icon> Create new Module
        </v-btn>
        <v-btn color="warning" :href="editContentURL" target="_blank">
          <v-icon left>edit</v-icon> Edit This content
        </v-btn>
      </v-flex>
      <v-flex shrink>
        <v-btn v-if="parent" exact dark :to="parent.link">
          <v-icon left>
            mdi-arrow-left
          </v-icon>{{ $t("actions.back") }}
        </v-btn>
        <v-btn v-else exact dark :to="{name:'help'}">
          <v-icon left>
            mdi-arrow-left
          </v-icon>{{ $t("actions.back") }}
        </v-btn>
      </v-flex>
    </v-layout>

    <!-- Course Modules grid -->
    <v-flex v-if="!isModule" xs12 xl8>
      <CourseModuleList :modules="modules" />
    </v-flex>

    <v-flex v-if="isModule" xs12 xl8 class="module-header">
      <!-- Top margin spacer -->
      <v-spacer class="my-5 py-5"></v-spacer>

      <!-- Course module Header -->
      <v-card flat dark :color="content.theme_color">
        <v-layout pa-0 ma-0 align-center justify-end wrap>
          <v-flex ma-1 pa-1 grow class="text-xs-center">
            <h1>{{ content.title }}</h1>
          </v-flex>

          <!-- This article in other languages -->
          <v-flex ma-1 pa-1 shrink>
            <v-menu v-if="courses.length > 0" offset-y>
              <v-btn slot="activator" outline class="white--text">
                {{ content.locale }}
                <v-icon right>
                  expand_more
                </v-icon>
              </v-btn>
              <v-list>
                <v-list-tile v-for="a in courses" :key="a.slug" :to="a.link">
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
          </v-flex>

        </v-layout>
      </v-card>
      <v-card flat>
        <v-card-text>
          <vue-markdown>{{ content.summary }}</vue-markdown>
        </v-card-text>
      </v-card>
    </v-flex>

    <!-- Content of the course split into sections -->
    <v-flex v-if="isModule" xs12 xl8 style="z-index:500">
      <CourseContent :key="content.id" :content="content" :parent="parent" :contents-same-master="courses" />
    </v-flex>

    <!-- Content of the Course Homepage -->
    <v-flex v-if="!isModule" xs12 xl8 style="z-index:500">
      <ArticleContent :key="content.id" :article="content" :articles-same-master="courses" />
    </v-flex>

    <v-flex v-if="isModule" xs12 xl8>
      <FeedbackForm :title="content.title" feedback-type="MODULE_FEEDBACK" model="content" :object-id="content.id" />
    </v-flex>

  </v-layout>
</template>

<script>
import CourseContent from "@/components/help/CourseContent";
import ArticleContent from "@/components/help/ArticleContent";
import CourseModuleList from "@/components/help/CourseModuleList";
import FeedbackForm from "@/components/input/FeedbackForm";
import { getFlagIso } from "@/plugins/i18n";
import { API_SERVER } from "@/plugins/resource";

export default {
  metaInfo() {
    return { title: this.content.title }
  },

  components: {
    ArticleContent,
    CourseContent,
    CourseModuleList,
    FeedbackForm
  },

  data() {
    return {
      courses: [],
      modules: [],
      getFlagIso,
    }
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
    contentSlug() {
      return this.$route.params.page;
    },
    createContentURL(){
      return API_SERVER + '/admin/backend/content/'
    },
    createModuleURL(){
      if(!this.content) return ''
      return API_SERVER + '/admin/backend/contentmaster/add/?type=MODULE&parent=' + this.content.master
    },
    editContentURL(){
      if(!this.content) return ''
      return API_SERVER + '/admin/backend/content/' + this.content.id + '/change/'
    },
    content(){
      return this.$store.getters["content/detail"](this.contentSlug);
    },
    isModule(){
      return this.content.hasOwnProperty('parent')
    },
    parent(){
      // TODO: select not the first in the list, but the one with the language we need
      if (this.isModule)
        return this.$store.getters["content/all"].filter(c => c.master == this.content.parent)[0]
      return null;
    }
  },

  async created(){
    this.$store.dispatch("content/clear")
    await this.loadContent()

    this.loadCourseModules()
    this.loadSameMasterContent()
  },

  methods:{
    async loadContent() {
      // load current article
      try {
        await this.$store.dispatch("content/load", [this.contentSlug]);
      } catch (error) {
          this.$router.push({ name: 'help' });
          this.$store.dispatch('toast/warning', this.$t('pages.help.articleDoesNotExist'))
      }
    },

    async loadSameMasterContent() {
      await this.$store.dispatch("content/load", {params:{master:this.content.master}});

      // Load master content
      if (this.isModule)
        await this.$store.dispatch("content/load", {params:{master:this.content.parent}});

      this.courses = this.$store.getters["content/all"].filter(c => c.master == this.content.master);
    },

    async loadCourseModules() {
      await this.$store.dispatch("content/load", {params:{master__parent:this.content.master, locale:this.content.locale}});
      this.modules = this.$store.getters["content/all"].filter(c => c.parent == this.content.master);
    },
  }
}
</script>

