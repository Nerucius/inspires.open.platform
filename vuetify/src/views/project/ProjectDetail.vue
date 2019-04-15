<style>
table{
  width: 100%;
}
table td, table th{
  padding: 0 8px 8px 8px;
}
table th{
  text-align: left;
}
table td{
  /* text-align: right */
}
</style>


<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex v-if="canManage" pa-0 xs12 class="text-xs-right">
      <v-btn flat outline color="warning" :to="manageLink">
        <v-icon left>
          edit
        </v-icon>Manage this Project
      </v-btn>
    </v-flex>

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
          <h1 class="title">
            {{ $t('pages.projectDetail.about') }}
          </h1>
        </v-toolbar>
        <v-card-text class="subheading">
          <table>
            <template v-if="project.contact_website">
              <tr>
                <th>{{ $t('forms.fields.contactWebsite') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="project.contact_website">
                    {{ project.contact_website }}
                  </a>
                </td>
              </tr>
            </template>

            <template v-if="project.contact_email">
              <tr>
                <th>{{ $t('forms.fields.email') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="'mailto:'+project.contact_email">
                    {{ project.contact_email }}
                  </a>
                </td>
              </tr>
            </template>

            <!-- Managers -->
            <!-- <tr>
              <th colspan="2">
                {{ $t('forms.fields.managers') }}:
              </th>
            </tr>
            <tr>
              <td colspan="2">
                <v-chip
                  v-for="uid in project.managers" :key="uid"
                  @click="$router.push({name:'account', params:{slug:obj2slug(user(uid), 'username')} })"
                >
                  <v-avatar>
                    <img :src="user(uid).avatar_url">
                  </v-avatar>
                  {{ user(uid).full_name }}
                </v-chip>
              </td>
            </tr> -->
            <!-- Participants -->
            <tr>
              <th colspan="2" style="text-align:left">
                {{ $t('forms.fields.participants') }}:
              </th>
            </tr>
            <tr>
              <td colspan="2">
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
        <v-img :src="project.image_url" height="200">
          <v-toolbar flat style="background-color:rgba(0,0,0,.3)" dark>
            <h1 class="title">
              {{ project.name }}
            </h1>
          </v-toolbar>
        </v-img>

        <v-card-text>
          <h2 class="headline mb-2">
            Summary
          </h2>
          <p>
            {{ project.summary }}
          </p>

          <h2 class="headline mb-2">
            Description
          </h2>
          <p v-html="$options.filters.nlbr(project.description)" />
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 md-8>
      <v-card flat>
        <v-card-text>
          <h2 class="headline mb-4">
            Related projects
          </h2>

          <ProjectCardHorizontal v-for="pid in project.related_projects" :key="pid" :project="getProject(pid)" />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>



<script>
import { slug2id, obj2slug } from "@/plugins/utils";
import ProjectCardHorizontal from "@/components/project/ProjectCardHorizontal";

export default {

  metaInfo(){
    return {
      title: (this.project || {}).name
    }
  },

  components:{
    ProjectCardHorizontal
  },

  data(){
    return {
      obj2slug,
      project: null,
    }
  },

  computed:{
    projectId(){
      return slug2id(this.$route.params.slug)
    },
    isApprovedProject(){
      return (this.project.collaboration != null && this.project.collaboration.is_approved)
    },
    manageLink() {
      return ({name:"project-manage", params:{slug:obj2slug(this.project)}})
    },
    canManage(){
      let userId = this.$store.getters['user/current'].id
      let isOwner = this.project.owner == userId
      let isAdmin = this.project.managers.filter(id => id == userId).length >  0
      return isOwner || isAdmin
    }
  },

  async mounted(){
    try{
      this.$store.dispatch("project/load")
      await this.$store.dispatch("project/load", [this.projectId])
      this.project = this.$store.getters['project/detail'](this.projectId)
    }catch(err){
      // TODO: Show error instead
      this.$router.push("/project-not-found")
    }
  },

  methods:{
    getProject(pid){
      return this.$store.getters["project/get"](pid)
    },

    user(uid){
      return this.$store.getters["user/get"](uid)
    },

    role(rid){
      if (rid==1) return "Sc"
      if (rid==2) return "St"
      if (rid==3) return "CS"
    }
  },

}
</script>
