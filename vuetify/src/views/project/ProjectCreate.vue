<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.projectCreate.title') }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <FormProjectBase
            @create="createProject($event)"
          />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import FormProjectBase from "@/components/project/FormProjectBase";
import { obj2slug } from "@/plugins/utils";

export default {

  metaInfo() {
    return {
      title: this.$t('pages.projectCreate.title')
    };
  },

  components:{
    FormProjectBase,
  },

  data(){
    return{
    }
  },

  methods: {

    async createProject(projectData){

      try{
        let project = await this.$store.dispatch("project/create", projectData)

        this.$matomo && this.$matomo.trackEvent('project', 'project--create')

        this.$store.dispatch("toast/success", this.$t('pages.projectCreate.success'))
        let slug = obj2slug(project)
        this.$router.push({name:"project-manage", params:{slug}})

      } catch(error){
        this.$store.dispatch("toast/error", {
          mesage:this.$t('pages.projectCreate.failure'),
          error
        })
      }

    }
  }
};
</script>
