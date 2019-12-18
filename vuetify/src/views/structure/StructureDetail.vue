<style scoped>
  .v-list__tile__title{
    font-weight: 500;
  }
</style>

<style>
  .v-list__tile__title p{
    margin-bottom: 0px;
  }

  /* Taller list elements */
  .v-list--two-line .v-list__tile{
    height: auto;
    min-height: 72px;
  }
</style>

<template>
  <v-layout v-if="structure" row wrap align-content-start>

    <v-flex v-if="canManage" pa-0 xs12 class="text-xs-right">
      <v-btn flat outline color="warning" :to="manageLink">
        <v-icon left>
          edit
        </v-icon>{{ $t('actions.manageName', {name: $t('noums.structure')}) }}
      </v-btn>
      <v-btn flat outline color="black" @click="exportCSV()">
        <v-icon left>
          mdi-database-export
        </v-icon>
        {{ $t('actions.exportAllData') }}
      </v-btn>
    </v-flex>

    <!-- Unvalidated Project Alert -->
    <v-flex v-if="!structure.validation" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>
          info
        </v-icon>
        {{ $t('pages.structureDetail.notApproved') }}
      </v-alert>
    </v-flex>

    <!-- About Sidebar -->
    <v-flex sm4 xs12>
      <v-card flat>
        <v-list two-line class="ma-0 pa-0">
          <v-toolbar dense flat color="primary" dark>
            <h1 class="title">
              {{ $t('pages.structureDetail.about') }}
            </h1>
          </v-toolbar>

          <!-- Contact Social Facebook -->
          <v-list-tile v-if="structure.contact_social_facebook" :href="structure.contact_social_facebook" target="_blank">
            <v-list-tile-avatar>
              <v-icon size="32" color="#3b5998">
                mdi-facebook
              </v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ structure.name }}
              </v-list-tile-title>
              <v-list-tile-sub-title>Facebook</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Social Twitter -->
          <v-list-tile v-if="structure.contact_social_twitter" :href="structure.contact_social_twitter" target="_blank">
            <v-list-tile-avatar>
              <v-icon size="32" color="#38A1F3">
                mdi-twitter
              </v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ structure.contact_social_twitter | twitterhandle }}
              </v-list-tile-title>
              <v-list-tile-sub-title>Twitter</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Social Other -->
          <v-list-tile v-if="structure.contact_social_other" :href="structure.contact_social_other" target="_blank">
            <v-list-tile-avatar>
              <v-icon size="32">
                mdi-account-group
              </v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ structure.name }}
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.socialNetwork') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Website -->
          <v-list-tile v-if="structure.contact_website">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="structure.contact_website">
                  {{ structure.contact_website }}
                </a>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.contactWebsite') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Email -->
          <v-list-tile v-if="structure.contact_email">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="`mailto:${structure.contact_email}`">
                  {{ structure.contact_email }}
                </a>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.contactEmail') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Address -->
          <v-list-tile v-if="structure.contact_postal_address">
            <v-list-tile-content>
              <v-list-tile-title style="height:auto">
                <vue-markdown>{{ structure.contact_postal_address }}</vue-markdown>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.postalAddress') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>


          <v-toolbar dense flat color="primary" dark class="mt-3">
            <h1 class="title">
              {{ $t('forms.fields.managers') }}
            </h1>
          </v-toolbar>

          <v-sheet :max-height="72*4.5" style="overflow-y:auto;">
            <template v-for="(manager, idx) in structure.managers">
              <v-list-tile :key="manager" :to="user(manager).link">
                <v-list-tile-avatar>
                  <v-img :src="user(manager).avatar_url" />
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ user(manager).full_name }}</v-list-tile-title>
                  <v-list-tile-sub-title />
                </v-list-tile-content>
              </v-list-tile>
              <v-divider v-if="idx != structure.managers.length - 1" :key="`div-${manager}`" />
            </template>
          </v-sheet>
        </v-list>
      </v-card>
    </v-flex>

    <!-- Main Body -->
    <v-flex xs12 sm8>
      <v-card flat>
        <v-img :src="structure.image_url" height="260">

          <v-layout ma-0 pa-0 justify-space-between column fill-height>
            <v-flex pa-0 shrink>
              <v-toolbar dense flat style="background-color:rgba(0,0,0,.3)" dark>
                <h1 class="title">
                  {{ structure.name }}
                </h1>
              </v-toolbar>
            </v-flex>

          <v-flex pa-0 shrink>
            <v-toolbar style="background-color:rgba(0,0,0,.3); white-space: nowrap" dense flat>
              <v-chip v-for="area in structure.knowledge_areas" :key="area.code"
                      dark color="grey darken-4"
                      :title="$t(ka(area).name)"
                      @click="$router.push(`/structures/areas/${obj2slug(ka(area))}`)"
              >
                {{ $t(ka(area).name) }}
              </v-chip>
            </v-toolbar>
          </v-flex>

          </v-layout>
        </v-img>

        <div class="px-4 pt-4 pb-2 grey lighten-4" style="font-spacing:110%">
          <vue-markdown>{{ structure.summary }}</vue-markdown>
        </div>

        <v-card-text>
          <vue-markdown>{{ structure.description }}</vue-markdown>
        </v-card-text>
      </v-card>
    </v-flex>

    <!-- Projects under the structure -->
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
import { API_SERVER } from "@/plugins/resource";

export default {

  metaInfo(){
    return {
      title: (this.structure || {}).name
    }
  },

  components:{
    ProjectCardHorizontal,
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

    exportLink(){
      // /v1/csv/export/5/structure_summary.csv
      return `${API_SERVER}/v1/csv/export/${this.structureId}/structure_summary.csv`
    },

    canManage(){
      let userId = this.$store.getters['user/current'].id
      let isOwner = this.structure.owner == userId
      let isAdmin = this.structure.managers.filter(id => id == userId).length >  0
      return isOwner || isAdmin
    }
  },

  async created(){
    try{
      await this.$store.dispatch("structure/load", [this.structureId])
      this.structure = this.$store.getters['structure/detail'](this.structureId)
      await this.$store.dispatch("project/load")
      await this.$store.dispatch("knowledgearea/load")
    }catch(err){
      // TODO: Show error instead
      this.$router.push("/structure-not-found")
    }
  },

  methods:{
    user(uid){
      return this.$store.getters["user/get"](uid)
    },

    ka(id){
      return this.$store.getters['knowledgearea/get'](id)
    },

    async exportCSV(){
      let data = (await this.$http.get(this.exportLink)).bodyText

      var file = new Blob([data], {type: "text/plain"});
      var filename = this.structure.name + " export.csv"

      if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
      else { // Others
          var a = document.createElement("a"),
                  url = URL.createObjectURL(file);
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          setTimeout(function() {
              document.body.removeChild(a);
              window.URL.revokeObjectURL(url);
          }, 0);
      }

    },
  },

}
</script>
