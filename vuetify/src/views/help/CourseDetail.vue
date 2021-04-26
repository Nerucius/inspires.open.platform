<template>
  <v-layout row wrap align-content-start justify-center>

  <v-flex xs12 xl8>
    <v-layout row wrap justify-end pa-2>
      <v-flex v-if="parent" grow pa-0 pl-1>
        <h1>{{ parent.title }}</h1>
      </v-flex>
      
      <v-flex v-else grow pa-0 pl-1>
        <h1>{{ $t("pages.help.title") }}</h1>
      </v-flex>
      
      <!-- Editor controls -->
      <v-flex v-if="currentUser.is_editor" shrink pa-0 >
        <v-btn v-if="!isModule" outline color="success" :href="createModuleURL" target="_blank">
          <v-icon left>add</v-icon> Create new Module
        </v-btn>
        <v-btn outline color="warning" :href="editContentURL" target="_blank">
          <v-icon left>edit</v-icon> Edit This content
        </v-btn>
      </v-flex>
    </v-layout>
  </v-flex>

  <v-flex xs12 xl8>
    <CourseContent :key="content.id" :content="content" :parent="parent" :contents-same-master="courses" />
  </v-flex>

  <v-flex xs12 xl8 v-if="!isModule">
    <CourseModuleList :modules="modules" />
  </v-flex>

  </v-layout>
</template>

<script>
import CourseContent from "@/components/help/CourseContent";
import CourseModuleList from "@/components/help/CourseModuleList";
import { getFlagIso } from "@/plugins/i18n";
import { API_SERVER } from "@/plugins/resource";

export default {
  metaInfo() {
    return { title: this.content.title }
  },

  data() {
    return {
      courses: [],
      modules: [],
      getFlagIso,
    }
  },

  components: {
    CourseContent,
    CourseModuleList
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

