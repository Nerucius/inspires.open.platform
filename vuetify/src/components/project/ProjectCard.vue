<style scoped>
  .v-image{ cursor: pointer; }
  h2 > a{
    text-decoration: none;
    color:inherit;
  }
</style>


<template>
  <v-card v-if="project.id">
    <v-img
      style="overflow: visible"
      :src="project.image_url"
      height="180"
      @click="$router.push(project.link)"
    >
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
      <!-- Project Title -->
      <v-sheet :height="26.5" class="overflow-hidden">
        <h2 style="font-size:125%" :title="project.name">
          <router-link :to="project.link">
            {{ project.name }}
            <small v-if="project.structure">
              | {{ project.structure.name }}
            </small>
          </router-link>
        </h2>
      </v-sheet>

      <!-- Project Area -->
      <v-btn
        v-if="project.knowledge_area"
        :to="kaLink(project.knowledge_area)" flat
        active-class="router-link"
        class="my-1 mx-0 pa-2 grey lighten-5 caption font-weight-light text-uppercase"
      >
        {{ $t(project.knowledge_area.name) }}
      </v-btn>
      <v-btn v-else disabled flat class="my-1 mx-0 pa-2 caption font-weight-light text-uppercase">
        {{ $t('pages.projectList.noKASpecified') }}
      </v-btn>

      <!-- Project Summary -->
      <v-sheet :height="4*21" class="overflow-hidden mb-2">
        {{ project.summary | ellipsis(200) }}
      </v-sheet>
    </v-card-text>

    <v-card-actions>
      <!-- <v-rating
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
      />-->
      <!-- <v-spacer /> -->

      <v-btn flat block :to="project.link">
        {{ $t('pages.projectList.visitProject') }}
      </v-btn>

      <!-- <v-btn flat
        :title="project.name"
        :to="project.link"
      >
        {{ $t('actions.more') }}
        <v-icon right class="hidden-sm-and-down">
          mdi-chevron-right
        </v-icon>
      </v-btn> -->
    </v-card-actions>
  </v-card>
</template>


<script>
import { obj2slug } from "@/plugins/utils";

export default {
  props: ['project'],

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
