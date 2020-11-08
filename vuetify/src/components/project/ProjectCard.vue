<style scoped>
  .v-image{ cursor: pointer; }
  h2 > a{
    text-decoration: none;
    color:inherit;
  }
</style>


<template>
  <v-card v-if="project.id" style="overflow: visible">
    <!-- Regular image view -->
    <template v-if="!showEvaluation">
      <v-img
        style="overflow: visible"
        :src="project.image_url"
        height="180"
        @click="$router.push(project.link)"
      >
        <!-- <v-btn flat absolute style="padding: 0; font-size:160%; top:0px; right: 0px">
        <flag :iso="iso3toiso2(project.country_code)" :squared="false"/>
        </v-btn> -->
        <!-- <v-btn
          flat absolute top right
          v-if="project.knowledge_area"
          :to="kaLink(project.knowledge_area)"
          active-class="router-link"
          class="mt-4 white lighten-5 caption font-weight-light text-uppercase"
        >
          {{ $t(project.knowledge_area.name) }}
        </v-btn> -->
        <v-btn
          v-for="(user,idx) in users(project.participants.slice(0,4))"
          :key="user.id"
          :to="user.link"
          icon
          fab
          absolute
          bottom
          right
          class="mb-3"
          :title="`${user.first_name} ${user.last_name}`"
          :style="`margin-right: ${idx*38}px`"
        >
          <v-avatar size="90%">
            <img :alt="user.username" :src="user.avatar_url+'&s=64'">
          </v-avatar>
        </v-btn>
      </v-img>

      <v-card-text class="pb-0">
        <v-sheet :height="7*21" class="overflow-hidden mb-2">
          <!-- Project Title -->
          <h2 style="font-size:125%" class="mb-2">
            <router-link :to="project.link">
              {{ project.name }}
              <small>
                <span v-if="project.structure">
                  | {{ project.structure.name }}
                </span>
                <span v-if="project.knowledge_area">
                  | {{ $t(project.knowledge_area.name) }}
                </span>
              </small>
            </router-link>
          </h2>

          <!-- Project Area -->
          <!-- <v-sheet >
          <v-btn
            v-if="project.knowledge_area"
            :to="kaLink(project.knowledge_area)" flat
            active-class="router-link"
            class="my-1 mx-0 pa-2 grey lighten-5 caption font-weight-light text-uppercase"
          >
            {{ $t(project.knowledge_area.name) }}
          </v-btn>
        </v-sheet>

        <v-sheet v-else height="36"></v-sheet> -->
          <!-- <v-btn v-else disabled flat class="my-1 mx-0 pa-2 caption font-weight-light text-uppercase">
          {{ $t('pages.projectList.noKASpecified') }}
        </v-btn> -->

          <!-- Project Summary -->
          {{ project.summary | ellipsis(200) }}
        </v-sheet>
      </v-card-text>
    </template>

    <!-- Evaluation tangram view -->
    <v-sheet v-else height="351" class="overflow-hidden">
      <v-sheet class="pa-2" height="260">
        <ProjectTangram :project="project">
          <v-layout fill-height column align-center justify-center>
            <v-flex shrink>
              <v-icon large>
                assignment_late
              </v-icon>
            </v-flex>
            <v-flex shrink>
              {{ $t('$vuetify.noDataText') }}
            </v-flex>
          </v-layout>
        </ProjectTangram>
      </v-sheet>

      <v-card-text class="pb-0">
        <v-sheet class="mb-2">
          <!-- Project Title -->
          <h2 style="font-size:125%" class="mb-2">
            <router-link :to="project.link" :title="project.name">
              {{ project.name }}
              <small>
                <span v-if="project.structure">
                  | {{ project.structure.name }}
                </span>
                <span v-if="project.knowledge_area">
                  | {{ $t(project.knowledge_area.name) }}
                </span>
              </small>
            </router-link>
          </h2>
        </v-sheet>
      </v-card-text>
    </v-sheet>

    <v-card-actions>
      <v-btn flat block :to="project.link">
        {{ $t('pages.projectList.visitProject') }}
      </v-btn>

      <!--
      <v-rating
        class="hidden-sm-and-down"
        readonly
        color="orange darken-3"
        background-color="orange darken-3"
        :value="project.rating"
      />
      <v-rating
        class="hidden-md-and-up"
        dense
        readonly
        color="orange darken-3"
        background-color="orange darken-3"
        :value="project.rating"
      />
      -->
    </v-card-actions>
  </v-card>
</template>


<script>
// import ProjectTangram from "@/components/evaluation/ProjectTangram";
// import { iso3toiso2, translateCountryName } from '@/plugins/countries'
import { obj2slug } from "@/plugins/utils";
import ProjectTangram from "@/components/evaluation/ProjectTangram";

export default {

  components:{
    ProjectTangram
  },
  props: ['project', 'showEvaluation'],

  data(){
    return{
    }
  },


  methods:{
    users(userIds){
      return userIds.map(uid => this.$store.getters["user/get"](uid) )
    },

    kaLink(knowledgeArea){
      let kaWithName = {...knowledgeArea, name: this.$t(knowledgeArea.name)}
      let area = obj2slug(kaWithName)
      return {name:"project-list-byarea", params:{area}}
    },

  }
};
</script>
