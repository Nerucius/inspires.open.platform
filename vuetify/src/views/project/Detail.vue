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
              <th>{{ $t('forms.fields.participants') }}:</th>
              <td>
                <v-chip
                  v-for="part in project.participants" :key="part.id"
                  @click="$router.push({name:'account', params:{slug:obj2slug(user(part.user), 'username')} })"
                >
                  <v-avatar>
                    <img :src="user(part.user).avatar_url">
                  </v-avatar>
                  {{ user(part.user).full_name }}
                  [ {{ part.role }} ]
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
import { slug2id, obj2slug } from "@/plugins/utils";

export default {

  data(){
    return {
      obj2slug,
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
    user(uid){
      return this.$store.getters["user/get"](uid)
    },
    users(userIds){
      return userIds.map(uid => this.$store.getters["user/get"](uid))
    }
  },

}
</script>
