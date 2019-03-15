<style>
table{
  width: 100%;
}
table td, table th{
  padding: 0 8px 8px 8px;
}
table th{
  text-align: right;
}
</style>


<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex xs12>
      <h1><small>Project |</small> {{ project.name }}</h1>
    </v-flex>

    <v-flex v-if="!isApprovedProject" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>
          info
        </v-icon>
        This project is not approved yet, it will not show up in public lists.
      </v-alert>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-toolbar dense flat color="primary" dark>
          <v-toolbar-title>{{ $t('pages.projectDetail.information') }}</v-toolbar-title>
        </v-toolbar>
        <v-card-text class="subheading">
          <table>
            <tr>
              <th>{{ $t('forms.fields.name') }}:</th>
              <td>{{ project.name }}</td>
            </tr>
            <tr>
              <th>{{ $t('forms.fields.summary') }}:</th>
              <td>{{ project.summary }}</td>
            </tr>
            <tr>
              <th>{{ $t('forms.fields.researchers') }}:</th>
              <td>
                <v-chip
                  v-for="user in users(project.researchers)" :key="user.id"
                  :to="{name:'login'}"
                >
                  <v-avatar>
                    <img :src="user.avatar_url" :alt="user.username">
                  </v-avatar>
                  {{ user.first_name }} {{ user.last_name }}
                </v-chip>
              </td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>



<script>
import { slug2id } from "@/plugins/utils";

export default {

  data(){
    return {
      project: null
    }
  },

  computed:{
    projectId(){
      return slug2id(this.$route.params.slug)
    },
    isApprovedProject(){
      return (this.project.collaboration != null && this.project.collaboration.is_approved)
    },
  },

  async mounted(){
    try{
      await this.$store.dispatch("project/load", [this.projectId])
      this.project = this.$store.getters['project/detail'](this.projectId)
    }catch(err){
      // TODO: Show error instead
      this.$router.push("/project-not-found")
    }
  },

  methods:{
    users(userIds){
      return userIds.map(uid => this.$store.getters["user/get"](uid))
    }
  },

}
</script>
