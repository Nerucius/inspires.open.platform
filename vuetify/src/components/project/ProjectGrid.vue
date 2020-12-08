<template>
  <v-layout row wrap align-content-start>
    <v-flex v-for="project in projects" :key="project.id" xs12 sm6 md4 lg3 xl2 mb-3>
      <ProjectCard :project="project" />
    </v-flex>
  </v-layout>
</template>

<script>
import ProjectCard from "@/components/project/ProjectCard";

export default {
  components:{
    ProjectCard
  },

  props: ["projects"],
};
</script>
