<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.projectManage.title') }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h3>
            Project Owner: {{ projectOwner.full_name }}
            <v-btn v-if="isOwner" flat>
              Transfer Ownership
            </v-btn>
          </h3>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <ProjectStructureForm
            :project-id="projectId"
            :processing="buttonLoading"
            @submit="createProjectCollaboration($event)"
          />
        </v-card-text>
      </v-card>
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

    <v-snackbar v-model="snackbar.active" top auto-height>
      {{ snackbar.message }}
      <v-btn color="pink" flat @click="snackbar.active = false">
        {{ $t('actions.close') }}
      </v-btn>
    </v-snackbar>
  </v-layout>
</template>

<script>
import ProjectForm from "@/components/project/ProjectForm";
import ProjectStructureForm from "@/components/project/ProjectStructureForm";
import { slug2id } from "@/plugins/utils";
import toastr from 'toastr'

export default {
  components: {
    ProjectForm,
    ProjectStructureForm,
  },

  data() {
    return {
      buttonLoading: false,
      snackbar: {
        message:"",
        active:false,
      },
    }
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    projectOwner(){
      let project = this.$store.getters["project/detail"](this.projectId)
      return this.$store.getters["user/get"](project.owner)
    },
    isOwner(){
      return this.projectOwner.id == this.$store.getters['user/current'].id
    }
  },

  async mounted() {
  },

  methods: {
    async updateProject(project) {
      this.buttonLoading = true
      this.snackbar.active = true
      try{
        await this.$store.dispatch("project/update", project)
        this.snackbar.message = this.$t('pages.projectManage.success')
      } catch(err){
        this.snackbar.message = this.$t('pages.projectManage.failure')
      }
      this.buttonLoading = false
    },

    async createProjectCollaboration(collaboration) {
      console.log(collaboration)
      this.buttonLoading = true
      this.snackbar.active = true
      try{
        await this.$store.dispatch("collaboration/create", collaboration)
        this.snackbar.message = this.$t('pages.projectManage.collaborationSuccess')
      } catch(err){
        this.snackbar.message = this.$t('pages.projectManage.collaborationFailure')
      }
      this.buttonLoading = false
    }
  }
};
</script>
