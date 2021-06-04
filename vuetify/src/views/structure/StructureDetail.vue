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
                        @click="$router.push(ka(area).link)"
                >
                  {{ $t(ka(area).name) }}
                </v-chip>
              </v-toolbar>
            </v-flex>
          </v-layout>
        </v-img>

        <v-tabs v-model="page.tab" grow>
          <v-tabs-slider color="primary" />
          <v-tab v-for="item in page.items" :key="item">
            {{ $t(item) }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="page.tab">
          <!-- About Tab -->
          <v-tab-item key="pages.structureDetail.about">
            <div class="px-4 pt-4 pb-2 grey lighten-4" style="font-spacing:110%">
              <vue-markdown>{{ structure.summary }}</vue-markdown>
            </div>
            <!-- Active country list -->
            <v-card-text v-if="structure.country_code != ''">
              <h3>{{ $tc('pages.structureDetail.activeCountries'
                , structure.country_code.split(',').length
                , {n : structure.country_code.split(',').length} ) }}</h3>
              <v-layout row wrap>
                <v-flex pa-0 ma-2 shrink v-for="cc in structure.country_code.split(',')" :key="cc">
                  <v-btn color="grey lighten-4" class="elevation-0 px-3 py-4" exact :to="{name:'structure-list', query:{country_code:cc}}">
                    <flag style="font-size:24px" :squared="false" :iso="iso3toiso2(cc)" />
                    <i class="mx-2"></i>
                    {{ countryTranslation(cc) }}
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-card-text>
            <v-card-text style="max-height:400px; overflow-y:auto">
              <vue-markdown>{{ structure.description }}</vue-markdown>
            </v-card-text>

          </v-tab-item>
          <!-- Files tab -->
          <v-tab-item key="noums.files">
            <v-card flat>
              <v-card-text class="px-0">
                <v-sheet class="grey lighten-4 pa-3 v-sheet theme--light">
                  <h2 class="mb-2">{{ $t('noums.files') }}</h2>
                  <p class="subheading">
                    {{ $t('pages.structureDetail.structureFiles') }}
                  </p>

                  <!-- List of attachments -->
                  <AttachmentList :attachments="structure.attachments" @change="reloadStructure" />
                  <!-- Upload form for editor -->
                  <template v-if="canManage">
                    <br>
                    <br>
                    <h3 mb-2>{{ $t('components.Attachment.upload') }}</h3>
                    <AttachmentUpload model="structure" :object-id="structure.id" @upload="reloadStructure" />
                  </template>
                </v-sheet>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>



      </v-card>
    </v-flex>

    <StructureNetworks :networks="networks" :skip="structure.id" />

    <!-- Projects under the structure -->
    <v-flex xs12>
      <h2 class="mb-2">{{ $t('noums.projects') }}</h2>
      <div class="hidden-sm-and-down">
        <ProjectGrid :hide-title="true" :projects="projects" />
      </div>
      <div class="hidden-md-and-up">
        <v-card>
          <ModelList show-last-modified="true" :objects="projects" />
        </v-card>
      </div>
    </v-flex>
  </v-layout>
</template>



<script>
import { iso3toiso2, translateCountryName } from '@/plugins/countries'
import { slug2id, obj2slug } from "@/plugins/utils";
import { API_SERVER } from "@/plugins/resource";

import ProjectGrid from "@/components/project/ProjectGrid";
import StructureNetworks from "@/components/structure/StructureNetworks";
import ModelList from "@/components/generic/ModelList";
import AttachmentUpload from "@/components/input/AttachmentUpload";
import AttachmentList from "@/components/attachment/AttachmentList";


export default {
  metaInfo() {
    return {
      meta: [
        {property: 'title', content: (this.structure || {}).name},
        {property: 'og:title', content: (this.structure || {}).name},
        {property: 'og:description', content: (this.structure || {}).summary},
        {property: 'og:image', content: (this.structure || {}).image_url},
        {property: 'og:type', content: 'website'},
      ]
    };
  },

  components:{
    ProjectGrid,
    ModelList,
    StructureNetworks,
    AttachmentList,
    AttachmentUpload,
  },

  data(){
    return {
      obj2slug,
      iso3toiso2,
      structure: null,
      page:{
        tab: null,
        items: [
          'pages.structureDetail.about',
          'noums.files',
        ]
      }
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
      return this.projectIds.map(id => this.$store.getters['project/detail'](id))
    },
    networks(){
      return this.structure.networks.map(id => this.$store.getters['network/detail'](id))
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
      await Promise.all([
        this.$store.dispatch("structure/load", [this.structureId]),
        // this.$store.dispatch("project/load"),
        this.$store.dispatch("knowledgearea/load"),
      ])

      this.structure = this.$store.getters['structure/detail'](this.structureId)

      // Load projects / networks related to this structure
      this.$store.dispatch('project/load', this.structure.collaborations.map(c => c.project))
      this.$store.dispatch("network/load", this.structure.networks)

    }catch(error){
        this.$store.dispatch("toast/error", {message: this.$t("errors.404.title"), error})
        this.$router.push({name:"structure-list"})
    }
  },

  methods:{
    user(uid){
      return this.$store.getters["user/get"](uid)
    },

    ka(id){
      return this.$store.getters['knowledgearea/get'](id)
    },

    countryTranslation(iso3){
      let locale = this.$i18n.locale
      return translateCountryName(iso3, locale);
    },

    async reloadStructure(){
      await this.$store.dispatch("strcture/load", [this.structureId])
      this.project = this.$store.getters["strcture/detail"](this.structureId);
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
