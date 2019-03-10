<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.projectManage.title') }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <ProjectForm
            :project-id="projectId"
            :processing="buttonLoading"
            @submit="updateProject($event)"
          />
        </v-card-text>
      </v-card>
    </v-flex>

    <v-snackbar v-model="snackbar" top auto-height>
      {{ $t('pages.projectManage.success') }}
      <v-btn color="pink" flat @click="snackbar = false">
        {{ $t('actions.close') }}
      </v-btn>
    </v-snackbar>
  </v-layout>
</template>

<script>
import ProjectForm from "@/components/project/ProjectForm";

export default {
  components: {
    ProjectForm
  },

  data() {
    return {
      buttonLoading: false,
      snackbar: false,
    }
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    }
  },

  async mounted() {
  },

  methods: {
    async updateProject(project) {
      this.buttonLoading = true
      this.snackbar = true
      await this.$store.dispatch("project/update", project)
      this.buttonLoading = false
    }
  }
};
</script>
