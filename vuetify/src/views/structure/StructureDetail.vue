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
</style>


<template>
  <v-layout v-if="structure" row wrap align-content-start>
    <v-flex v-if="canManage" pa-0 xs12 class="text-xs-right" >
      <v-btn flat outline color="warning" :to="manageLink">
        <v-icon left>
          edit
        </v-icon>Manage this Structure
      </v-btn>
    </v-flex>

    <!-- Not validated Alert -->
    <v-flex v-if="!structure.validation" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>
          info
        </v-icon>
        This structure is not approved yet, it will not show up in public lists.
      </v-alert>
    </v-flex>


    <v-flex sm4 xs12>
      <v-card flat>
        <v-toolbar dense flat color="primary" dark>
          <h1 class="title">
            {{ $t('pages.structureDetail.about') }}
          </h1>
        </v-toolbar>
        <v-card-text class="subheading">
          <table>
            <template v-if="structure.contact_website">
              <tr>
                <th>{{ $t('forms.fields.contactWebsite') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="structure.contact_website">
                    {{ structure.contact_website }}
                  </a>
                </td>
              </tr>
            </template>

            <template v-if="structure.contact_email">
              <tr>
                <th>{{ $t('forms.fields.email') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="'mailto:'+structure.contact_email">
                    {{ structure.contact_email }}
                  </a>
                </td>
              </tr>
            </template>

            <template v-if="structure.contact_postal_address">
              <tr>
                <th>{{ $t('forms.fields.postalAddress') }}:</th>
              </tr>
              <tr>
                <td colspan="2"
                    :inner-html.prop="structure.contact_postal_address | nlbr"
                />
              </tr>
            </template>

            <!-- Managers -->
            <tr>
              <th colspan="2" style="text-align:left">
                {{ $t('forms.fields.managers') }}:
              </th>
            </tr>
            <tr>
              <td colspan="2">
                <v-chip
                  v-for="uid in structure.managers" :key="uid"
                  @click="$router.push({name:'account', params:{slug:obj2slug(user(uid), 'username')} })"
                >
                  <v-avatar>
                    <img :src="user(uid).avatar_url">
                  </v-avatar>
                  {{ user(uid).full_name }}
                </v-chip>
              </td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 sm8>
      <v-card flat>
        <v-img :src="structure.image_url" height="200">
          <v-toolbar dense flat style="background-color:rgba(0,0,0,.3)" dark>
            <h1 class="title">
              {{ structure.name }}
            </h1>
          </v-toolbar>
        </v-img>

        <v-card-text>
          <h2 class="headline mb-2">
            Introduction
          </h2>
          <p class="subheading">
            {{ structure.summary }}
          </p>

          <h2 class="headline mb-2">
            About Us
          </h2>
          <p class="subheading" :inner-html.prop="structure.description | nlbr" />
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="headline mb-2">
            Projects under this Structure
          </h2>

          <p class="subheading mb-5">
            Overview of all the projects that are nested under this structure.
          </p>

          <ProjectCardHorizontal v-for="project in projects" :key="project.id" :project="project" />
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
      title: (this.structure || {}).name
    }
  },

  components:{
    ProjectCardHorizontal
  },

  data(){
    return {
      obj2slug,
      structure: null
    }
  },

  computed:{
    structureId(){
      return slug2id(this.$route.params.slug)
    },
    projectIds(){
      return this.structure.collaborations.filter(c => c.is_approved).map(c => c.project)
    },
    projects(){
      return this.projectIds.map(pid => this.$store.getters['project/get'](pid))
    },
    isApprovedStructure(){
      return true
    },
    manageLink() {
      return ({name:"structure-manage", params:{slug:obj2slug(this.structure)}})
    },
    canManage(){
      let userId = this.$store.getters['user/current'].id
      let isOwner = this.structure.owner == userId
      let isAdmin = this.structure.managers.filter(id => id == userId).length >  0
      return isOwner || isAdmin
    }
  },

  async mounted(){
    try{
      await this.$store.dispatch("structure/load", [this.structureId])
      this.structure = this.$store.getters['structure/detail'](this.structureId)
      await this.$store.dispatch("project/load")
    }catch(err){
      // TODO: Show error instead
      this.$router.push("/structure-not-found")
    }
  },

  methods:{
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
