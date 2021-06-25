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

  .editor--controls .v-btn--outline{
    background-color: rgba(255,255,255,0.8) !important;
  }
</style>

<template>
  <v-layout row wrap align-content-start justify-center>

    <!-- Module Cover Image -->
    <v-parallax
      class="cover-image"
      height="800"
      :src="content.image_url"
    />

    <!-- TODO: Header across the top with all modules -->
    <!-- <div class="cover-image">
    </div> -->

    <!-- Navigation Buttons -->
    <v-flex xs12 xl8>
      <!-- Top margin spacer -->
      <v-layout justify-start>

        <!-- Editor controls -->
        <v-flex v-if="currentUser.is_editor" shrink class="editor--controls">
          <v-speed-dial
            v-model="speeddial"
            direction="bottom"
          >
            <template v-slot:activator>
              <v-btn color="red darken-2" dark>
                <v-icon v-if="!speeddial" left>edit</v-icon>
                <v-icon v-if="speeddial" left>close</v-icon>
                Editor Tools
              </v-btn>
            </template>

            <v-btn v-if="!isModule" outline round color="success" :href="createModuleURL" target="_blank">
              <v-icon left>add</v-icon> New Module
            </v-btn>
            <v-btn color="success" outline round :href="createContentVariantURL" target="_blank">
              <v-icon left>add</v-icon> New Language
            </v-btn>
            <v-btn color="warning" outline round :href="editContentURL" target="_blank">
              <v-icon left>edit</v-icon> Edit
            </v-btn>

          </v-speed-dial>
        </v-flex>

        <v-spacer />

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

      <v-spacer class="hidden-xs-only my-5 py-5" />
    </v-flex>

    <!-- Content of the Course Page -->
    <template v-if="!!content && !isModule">
      <v-flex xs12 xl8 style="z-index:500">
        <ArticleContent :key="content.id" :article="content" :articles-same-master="courses" />
      </v-flex>

      <v-flex xs12 xl8>
        <CourseModuleList :modules="modules" />
      </v-flex>
    </template>

    <!-- Content of the Module Page -->
    <template v-if="!!content && isModule">
      <!-- Course module Header -->
      <v-flex xs12 xl8 class="module-header">


        <v-card flat dark :color="content.theme_color">
          <v-layout pa-0 ma-0 align-center justify-end wrap>
            <v-flex ma-1 pa-1 grow class="text-xs-center">
              <h1>{{ content.title }}</h1>
            </v-flex>

            <!-- This article in other languages -->
            <v-flex ma-1 pa-1 shrink>
              <v-menu offset-y>
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
            <!-- Last modified -->
            <div class="text-xs-right grey--text body-1">
              <span :title="moment(content.modified_at).format('L LT')">
                {{
                  $t("misc.lastUpdated", {
                    time: moment(content.modified_at).fromNow(),
                  })
                }}
              </span>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>

      <!-- Content of the course split into sections -->
      <v-flex xs12 xl8 style="z-index:500">
        <CourseContent :key="content.id" :content="content" :parent="parent" :contents-same-master="courses" />
      </v-flex>
    </template>

    <template v-if="!!content">
      <!-- Attached Materials -->
      <v-flex xs12 xl8>
        <AttachmentMenu :expanded="content.attachments.length > 0" :content="content" @change="loadContent" />
      </v-flex>

      <!-- Feedback form (Modules Only) -->
      <v-flex v-if="isModule" xs12 xl8>
        <FeedbackForm :title="content.title" feedback-type="MODULE_FEEDBACK" model="content" :object-id="content.id" />
      </v-flex>
    </template>

  </v-layout>
</template>

<script>
import CourseContent from "@/components/help/CourseContent";
import ArticleContent from "@/components/help/ArticleContent";
import CourseModuleList from "@/components/help/CourseModuleList";
import FeedbackForm from "@/components/input/FeedbackForm";
import AttachmentMenu from "@/components/attachment/AttachmentMenu";

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
    FeedbackForm,
    AttachmentMenu,
  },

  data() {
    return {
      moment,
      speeddial: false,
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
    createContentVariantURL(){
      if(!this.content) return ''
      return API_SERVER + `/admin/backend/content/add/?master=${this.content.master}`
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

