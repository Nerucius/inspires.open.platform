<template>
  <v-card flat>
    <v-card-text>
      <h1 class="mb-2" v-if="!hideTitle">
        {{ $t('noums.projects') }}
      </h1>

      <!-- <v-container grid-list-xl> -->
      <v-layout row wrap>
        <v-flex v-for="project in projects" :key="project.id" xs12 sm6 md4 lg3 xl2 mb-3>
          <ProjectCard :project="project" />
        </v-flex>
      </v-layout>
      <!-- </v-container> -->
    </v-card-text>
  </v-card>
</template>

<script>
import ProjectCard from "@/components/project/ProjectCard";

export default {

  components:{
    ProjectCard
  },

  props: ["projects", "hideTitle"],

  data() {
    return {
    }
  },

  methods: {
  }
};
</script>
