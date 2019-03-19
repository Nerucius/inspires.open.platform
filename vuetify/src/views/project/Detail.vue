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

    <v-flex v-if="!isApprovedProject" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>
          info
        </v-icon>
        This project is not approved yet, it will not show up in public lists.
      </v-alert>
    </v-flex>

    <v-flex sm4 class="hidden-xs-only">
      <v-card flat>
        <v-toolbar dense flat color="primary" dark>
            <h1 class="title">{{ $t('pages.projectDetail.information') }}</h1>
        </v-toolbar>
        <v-card-text class="subheading">
          <table>
            <!-- Managers -->
            <tr>
              <th colspan="2" style="text-align:left">
                {{ $t('forms.fields.managers') }}:
              </th>
            </tr>
            <tr>
              <td colspan="2" >
                <v-chip
                  v-for="user in users(project.managers)" :key="user.id"
                  @click="$router.push({name:'account', params:{slug:obj2slug(user, 'username')} })"
                >
                  <v-avatar>
                    <img :src="user.avatar_url">
                  </v-avatar>
                  {{ user.full_name }}
                </v-chip>
              </td>
            </tr>
            <!-- Participants -->
            <tr>
              <th colspan="2" style="text-align:left">
                {{ $t('forms.fields.participants') }}:
              </th>
            </tr>
            <tr>
              <td colspan="2" >
                <v-chip
                  v-for="part in project.participants" :key="part.id"
                  @click="$router.push({name:'account', params:{slug:obj2slug(user(part.user), 'username')} })"
                >
                  <v-avatar>
                    <img :src="user(part.user).avatar_url">
                  </v-avatar>
                  {{ user(part.user).full_name }}
                   ({{ role(part.role) }})
                </v-chip>
              </td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 sm8>
      <v-card flat>


        <v-img :src="project.image_url || defaultImage" height="200">
          <v-toolbar dense flat style="background-color:rgba(0,0,0,.3)" dark>
              <h1 class="title">{{ project.name }}</h1>
          </v-toolbar>
        </v-img>

        <v-card-text>
          <h2 class="headline">Summary</h2>
          <p>
            {{project.summary}}
          </p>

          <h2 class="headline">Description</h2>
          <p>
            {{project.description}}
          </p>

          <h2 class="headline">Related projects</h2>
          <p>
          </p>

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
      project: null,
      defaultImage : "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg"
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
    },

    role(rid){
      if (rid==1) return "Sc"
      if (rid==2) return "St"
      if (rid==3) return "CS"
    }
  },

}
</script>
