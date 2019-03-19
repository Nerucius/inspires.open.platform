<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>Create new Project</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <FormProjectBase
            :processing="buttonLoading"
            @submit="createProject($event)"
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
import FormProjectBase from "@/components/project/FormProjectBase";
import { obj2slug } from "@/plugins/utils";

export default {

  components:{
    FormProjectBase,
  },

  data(){
    return{
      buttonLoading: false,
      snackbar: {
        message:"",
        active:false,
      },
    }
  },

  methods: {

    async createProject(projectData){
      this.buttonLoading = true
      this.snackbar.active = true

      try{
        let project = await this.$store.dispatch("project/create", projectData)
        this.snackbar.message = this.$t('pages.projectCreate.success')
        let slug = obj2slug(project)
        this.$router.push({name:"project-manage", params:{slug}})

      } catch(err){
        console.log(err)
        this.snackbar.message = this.$t('pages.projectCreate.failure')
      }

      this.buttonLoading = false
    }

  }
};
</script>
