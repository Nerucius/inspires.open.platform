<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <ProjectGrid :projects="projects" />
    </v-flex>
  </v-layout>
</template>


<script>
import ProjectGrid from "@/components/project/ProjectGrid";

export default {
  components: {
    ProjectGrid
  },

  data() {
    return {};
  },

  computed: {
    projects() {
      return this.$store.getters["project/all"];
    }
  },

  mounted(){
    this.$store.dispatch("project/load", {params:{limit:20}})
  }
};
</script>

