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
  <v-layout v-if="project.id" row wrap align-content-start>
    <v-flex xs12>
      <h1><small>Project |</small> {{ project.name }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-card>
        <v-toolbar dense flat color="teal darken-2" dark>
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
export default {

  data(){
    return {

    }
  },

  computed:{
    project(){
      return this.$store.getters['project/detail'](this.projectId)
    },
    projectId(){
      return this.$route.params.id.split('-')[0]
    }
  },

  async mounted(){
    this.$store.dispatch("project/load", [this.projectId])
  },

  methods:{
    users(userIds){
      return userIds.map(uid => this.$store.getters["user/get"](uid))
    }
  },

}
</script>
