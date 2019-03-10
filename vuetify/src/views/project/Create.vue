<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>Create new Project</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <ProjectForm @submit="createProject($event)" />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import ProjectForm from "@/components/project/ProjectForm";

export default {

  components:{
    ProjectForm,
  },

  methods: {

    createProject(project){
      console.log(project)
      // this.$store.dispatch("project/create", project)
    }

  }
};
</script>
