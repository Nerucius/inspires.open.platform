<style scoped>
  table {
    width: 100%;
  }
  table td,
  table th {
    padding: 0 8px 8px 8px;
  }
  table th {
    text-align: left;
  }
  .v-chip__content {
    cursor: pointer !important;
    text-decoration: none !important;
  }

  .person-slab a{
    color: white;
    text-decoration: none;
    text-shadow: 1px 1px 2px #000;
  }

  .v-list__tile__title{
    font-weight: 500;
  }
</style>

<style scoped>
  /* .v-image{ cursor: pointer; } */
  .circle{
    width: 24px;
    height: 24px;
    border: 1px solid darkslategray;
    border-radius: 100%;
    overflow:hidden;
  }

  .circle .circle__padding{
    width: 22px;
    height: 22px;
    border: 2px solid white;
    border-radius: 100%;
    overflow:hidden;

    display: flex;
    align-items: flex-end;
  }

  .circle .circle__fill{
    width: 20px;
    height: 20px;
  }

  .circle .circle__fill.p0{
    background-color: teal;
  }

  .circle .circle__fill.p1{
    background-color: teal;
  }

  .circle .circle__fill.p2{
    background-color: teal;
  }

  .circle .circle__fill.p3{
    background-color: teal;
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
  <v-layout v-if="project" row wrap align-content-start>

    <!-- Manage / Export buttons -->
    <v-flex v-if="canManage" pa-0 xs12 class="text-xs-right">
      <v-btn flat outline color="warning" :to="manageLink">
        <v-icon left>
          edit
        </v-icon>{{ $t('actions.manageName', {name: $t('noums.project')}) }}
      </v-btn>
      <v-btn flat outline color="black" @click="exportCSV()">
        <v-icon left>
          mdi-database-export
        </v-icon>
        {{ $t('actions.exportAllData') }}
      </v-btn>
    </v-flex>

    <!-- Unapproved Project Alert -->
    <v-flex v-if="!isApprovedProject" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>
          info
        </v-icon>
        {{ $t('pages.projectDetail.notApproved') }}
      </v-alert>
    </v-flex>

    <!-- About Sidebar -->
    <v-flex sm4 xs12 class="_no-hidden-xs-only">
      <v-card flat>
        <v-list two-line class="ma-0 pa-0">
          <v-toolbar dense flat color="primary" dark>
            <h1 class="title">
              {{ $t('pages.projectDetail.about') }}
            </h1>
          </v-toolbar>

          <!-- Structure -->
          <v-list-tile v-if="structure" :to="structure.link">
            <v-list-tile-avatar tile>
              <v-img :src="structure.image_url" />
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ structure.name }}</v-list-tile-title>
              <v-list-tile-sub-title><b>{{ $t('noums.mainStructure') }}</b></v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <template v-if="!!partnerStructures && partnerStructures.length > 0">

            <v-list-tile v-for="partner in partnerStructures" :key="partner.id" :to="partner.link">
              <v-list-tile-avatar tile class="px-3">
                <v-img :src="partner.image_url" />
              </v-list-tile-avatar>
              <v-list-tile-content>
                <v-list-tile-title>{{ partner.name }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ $t('noums.partnerStructure') }}</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>

          </template>

          <!-- Knowledge Area -->
          <v-list-tile v-if="project.knowledge_area">
            <v-list-tile-avatar tile>
              <v-icon>mdi-school</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ knowledgeAreaTL(project.knowledge_area) }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.knowledgeArea') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Project Type -->
          <v-list-tile v-if="project.project_type">
            <v-list-tile-avatar tile>
              <v-icon>mdi-office-building</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ projectTypeTL(project.project_type) }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.projectType') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Social Facebook -->
          <v-list-tile v-if="project.contact_social_facebook" :href="project.contact_social_facebook" target="_blank">
            <v-list-tile-avatar>
              <v-icon size="32" color="#3b5998">
                mdi-facebook
              </v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ project.name }}
              </v-list-tile-title>
              <v-list-tile-sub-title>Facebook</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Social Twitter -->
          <v-list-tile v-if="project.contact_social_twitter" :href="project.contact_social_twitter" target="_blank">
            <v-list-tile-avatar>
              <v-icon size="32" color="#38A1F3">
                mdi-twitter
              </v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ project.contact_social_twitter | twitterhandle }}
              </v-list-tile-title>
              <v-list-tile-sub-title>Twitter</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Social Other -->
          <v-list-tile v-if="project.contact_social_other" :href="project.contact_social_other" target="_blank">
            <v-list-tile-avatar>
              <v-icon size="32">
                mdi-account-group
              </v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ project.name }}
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.socialNetwork') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Website -->
          <v-list-tile v-if="project.contact_website">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="project.contact_website">
                  {{ project.contact_website }}
                </a>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.contactWebsite') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Email -->
          <v-list-tile v-if="project.contact_email">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="`mailto:${project.contact_email}`">
                  {{ project.contact_email }}
                </a>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.contactEmail') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Address -->
          <v-list-tile v-if="project.contact_postal_address">
            <v-list-tile-content>
              <v-list-tile-title style="height:auto; padding-top:4px">
                <vue-markdown>{{ project.contact_postal_address }}</vue-markdown>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.postalAddress') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Project participants -->
          <v-toolbar dense flat color="primary" dark class="mt-3">
            <h1 class="title">
              {{ $t('forms.fields.participants') }}
            </h1>
          </v-toolbar>
          <v-sheet :max-height="72*10.5" style="overflow-y:auto;">
            <template v-for="(part, idx) in project.participants">
              <v-list-tile :key="part.id" :to="user(part.user).link">
                <v-list-tile-avatar>
                  <v-img :src="user(part.user).avatar_url" />
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ user(part.user).full_name }}</v-list-tile-title>
                  <v-list-tile-sub-title>
                    {{ $t(role(part.role).name) }}
                  </v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-divider v-if="idx != project.participants.length - 1" :key="`div-${part.id}`" />
            </template>
          </v-sheet>

        </v-list>
      </v-card>
    </v-flex>

    <!-- Main Body -->
    <v-flex xs12 sm8>
      <v-img :src="project.image_url" height="260">
        <v-toolbar flat style="background-color:rgba(0,0,0,.3)" dark>
          <h1 class="title">
            {{ project.name }}
          </h1>
        </v-toolbar>
      </v-img>

      <!-- Tabs menu -->
      <v-tabs v-model="page.tab" grow>
        <v-tabs-slider color="primary" />
        <v-tab v-for="item in page.items" :key="item">
          {{ $t(item) }}
        </v-tab>
      </v-tabs>

      <!-- Main Body -->
      <v-tabs-items v-model="page.tab">
        <!-- TAB: Project Details -->
        <v-tab-item key="pages.projectDetail.about">
          <v-card flat>
            <div class="py-1 px-3 text-xs-right">
              <small>
                {{ $t('misc.lastUpdated', {time: moment(project.modified_at).fromNow()}) }}
              </small>
            </div>
            <div class="px-4 pt-4 pb-2 grey lighten-4 subheading" style="font-spacing:110%">
              <vue-markdown>{{ project.summary }}</vue-markdown>
            </div>

            <!-- Active country list -->
            <v-card-text v-if="project.country_code">
              <h3>{{ $tc('pages.projectDetail.activeCountries'
                , project.country_code.split(',').length
                , {n : project.country_code.split(',').length} ) }}</h3>
              <v-layout row wrap>
                <v-flex pa-0 ma-2 shrink v-for="cc in project.country_code.split(',')" :key="cc">
                  <v-btn color="grey lighten-4" class="elevation-0 px-3 py-4" exact :to="{name:'project-list', query:{country_code:cc}}">
                    <flag style="font-size:24px" :squared="false" :iso="iso3toiso2(cc)" />
                    <i class="mx-2"></i>
                    {{ countryTranslation(cc) }}
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-card-text>

            <v-card-text>
              <vue-markdown>{{ project.description }}</vue-markdown>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- TAB: Project Evaluation -->
        <v-tab-item key="pages.projectDetail.evaluationTab">
          <v-card flat>
            <v-card-text>
              <h2 class="mb-2">
                {{ $t('pages.projectDetail.evaluationTab') }}
              </h2>

              <div v-if="isParticipant">
                <p>Since you are a participant of this project, you can view the detailed evaluation results at this page:</p>
                <p class="text-xs-center">
                  <v-btn dark color="grey darken-3"
                        :to="{...project.link, name:'evaluation-detail'}"
                        class="elevation-0"
                  >
                    <v-icon left>mdi-school</v-icon>
                    {{ $t('pages.projectManage.evalViewEvaluationResults') }}
                  </v-btn>
                </p>

                <p>{{ $t('pages.evaluationEntry.selfQuestionnaireDescription') }}</p>

                <p class="text-xs-center">
                  <v-btn dark color="blue darken-1" href="/learn/?master=12">
                    <v-icon left>mdi-file-pdf</v-icon>
                    {{ $t('pages.evaluationEntry.viewQuestionnaire1') }}
                  </v-btn>
                  <br>
                  <v-btn dark color="green darken-2" href="/learn/?master=13">
                    <v-icon left>mdi-file-pdf</v-icon>
                    {{ $t('pages.evaluationEntry.viewQuestionnaire3') }}
                  </v-btn>
                </p>

                <!-- <p class="text-xs-center">
                  <v-btn dark color="red" href="https://app.inspiresproject.com/uploads/inspires-self-questionaire.pdf" target="_blank">
                    <v-icon left>mdi-file-pdf</v-icon>
                    {{ $t('actions.downloadName', {name: $t('pages.evaluationEntry.selfQuestionnaireTitle')}) }}
                  </v-btn>
                </p> -->
                <hr class="my-5">
              </div>

              <!-- Public Evaluation Results -->
              <v-layout wrap>
                <v-flex xs12 lg6 py-5>
                  <h3 class="text-xs-center">{{ project.name }}</h3>
                  <ProjectTangram :project="project">
                    <div class="subheading py-4">
                      {{ $t('pages.projectDetail.projectNotYetEvaluated') }}
                    </div>
                  </ProjectTangram>

                  <!-- TODO: move this to own component -->
                  <div style="display:flex; justify-content:space-around">
                    <div style="flex: 0 0 auto; display:flex">
                      <!-- Filled bullets -->
                      <div v-for="(p,idx) in evalStats.statPhases" :key="idx" style="flex: 0 0 auto; margin: 0 8px">
                        <div class="circle" :title="$t(`models.projectPhase.phase${idx+1}Tag`)">
                          <div class="circle__padding">
                            <div :class="{circle__fill:true, ['p'+idx]:true}" :style="{height: p*14+'px'}" />
                          </div>
                        </div>
                      </div>
                    </div>
                    <div :title="$t('components.ProjectCard.numberOfParticipants')" style="flex: 0 0 auto; line-height:22px; font-size: 20px;">
                      N:<b>{{ evalStats.statN }}</b>
                    </div>
                  </div>

                </v-flex>
                <v-flex xs12 lg6>
                  <h3 class="mb-2">Reading the Hummingbird</h3>
                  <vue-markdown>{{ $t('pages.evaluationDetail.help.publicEval') }}</vue-markdown>
                </v-flex>

                <v-flex xs12>
                  <h3 class="mb-2">Phase Participation points</h3>
                  <vue-markdown>{{ $t('pages.evaluationDetail.help.phaseParticipation') }}</vue-markdown>
                </v-flex>
              </v-layout>

            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- TAB: Files -->
        <v-tab-item key="noums.files">
          <v-card flat>
            <v-card-text class="px-0">
              <v-sheet class="grey lighten-4 pa-3 v-sheet theme--light">
                <h2 class="mb-2">{{ $t('noums.files') }}</h2>
                <p class="subheading">
                  {{ $t('pages.projectDetail.projectFiles') }}
                </p>

                <!-- List of attachments -->
                <AttachmentList :attachments="project.attachments" @change="reloadProject" />
                <!-- Upload form for editor -->
                <template v-if="canManage">
                  <br>
                  <br>
                  <h3 mb-2>{{ $t('components.Attachment.upload') }}</h3>
                  <AttachmentUpload model="project" :object-id="project.id" @upload="reloadProject" />
                </template>
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-tab-item>

      </v-tabs-items>
    </v-flex>


    <!-- Related Projects -->
    <v-flex v-if="project.related_projects.length > 0" xs12 md-8>
      <v-card flat>
        <v-card-text>
          <h2 class="headline mb-4">
            Related projects
          </h2>

          <ProjectCardHorizontal
            v-for="pid in project.related_projects"
            :key="pid"
            :project="getProject(pid)"
          />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>


<script>
import { iso3toiso2, translateCountryName } from '@/plugins/countries'
import { slug2id, obj2slug, onlyUnique } from "@/plugins/utils";
import { API_SERVER } from "@/plugins/resource";
import { ProjectEvaluationStatsResource } from "@/plugins/resource";

import AttachmentUpload from "@/components/input/AttachmentUpload";
import AttachmentList from "@/components/attachment/AttachmentList";
import ProjectCardHorizontal from "@/components/project/ProjectCardHorizontal";
import ProjectTangram from "@/components/evaluation/ProjectTangram";


export default {
  metaInfo() {
    return {
      meta: [
        {property: 'title', content: (this.project || {}).name},
        {property: 'og:title', content: (this.project || {}).name},
        {property: 'og:description', content: (this.project || {}).summary},
        {property: 'og:image', content: (this.project || {}).image_url},
        {property: 'og:type', content: 'website'},
      ]
    };
  },

  components: {
    ProjectCardHorizontal,
    ProjectTangram,
    AttachmentList,
    AttachmentUpload,
  },

  data() {
    return {
      moment,
      obj2slug,
      iso3toiso2,
      project: null,
      structure: null,
      partnerStructures: null,
      evalStats : [],
      page:{
        tab: null,
        items:[
          'pages.projectDetail.about',
          'pages.projectDetail.evaluationTab',
          'noums.files',
        ]
      }
    };
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    isApprovedProject() {
      return (
        this.project.collaboration != null &&
        this.project.collaboration.is_approved
      );
    },
    manageLink() {
      return {
        name: "project-manage",
        params: { slug: obj2slug(this.project) }
      };
    },
    exportLink(){
      // /v1/csv/export/5/structure_summary.csv
      return `${API_SERVER}/v1/csv/export/${this.projectId}/project_summary.csv`
    },

    canManage() {
      let userId = this.$store.getters["user/current"].id;
      let isOwner = this.project.owner == userId;
      let isAdmin = this.project.managers.filter(id => id == userId).length > 0;
      return isOwner || isAdmin;
    },

    isParticipant(){
      let user = this.$store.getters['user/current']
      if (user.id == -1) return false;
      let pids = [
        ...user.owned_projects,
        ...user.managed_projects,
        ...user.researched_projects,
      ]
      return pids.indexOf(this.project.id) > -1
    }

  },

  async created() {
    try {
      // Load data
      await Promise.all([
        this.$store.dispatch("project/load"),
        this.$store.dispatch("knowledgearea/load"),
        this.$store.dispatch("project/load", [this.projectId]),
      ])

      this.project = this.$store.getters["project/detail"](this.projectId);

      // If project has a collaboration, load related structures
      if(this.project.collaboration){
        let structureId = this.project.collaboration.structure
        let partnerStructureIds = this.project.collaboration.partners

        console.log([structureId, ...partnerStructureIds]);

        await this.$store.dispatch("structure/load", [structureId,...partnerStructureIds]);

        this.structure = this.$store.getters['structure/detail'](structureId)
        this.partnerStructures = partnerStructureIds.map(sid => this.$store.getters['structure/detail'](sid))
      }


    } catch (error) {
      this.$store.dispatch('toast/error', {message:this.$t('pages.projectDetail.projectNotFound'),error})
      this.$router.push({name:"project-list"})
    }

    this.loadEvaluation();
  },

  methods: {
    roleBg(roleId){
      return this.$store.getters['evaluation/roles'][roleId].bg
    },

    getProject(pid) {
      return this.$store.getters["project/get"](pid);
    },

    user(uid) {
      return this.$store.getters["user/get"](uid);
    },

    role(rid) {
      return this.$store.getters["evaluation/roles"][rid];
    },

    countryTranslation(iso3){
      let locale = this.$i18n.locale
      return translateCountryName(iso3, locale);
    },

    projectTypeTL(ptId){
      let pt = this.$store.getters['project/projectTypes'].filter(pt => pt.value == ptId)[0];

      return this.$t(pt.name);
    },

    knowledgeAreaTL(kaId){
      let ka = this.$store.getters['knowledgearea/get'](kaId)

      return this.$t(ka.name)
    },

    async reloadProject(){
      await this.$store.dispatch("project/load", [this.projectId])
      this.project = this.$store.getters["project/detail"](this.projectId);
    },

    async loadEvaluation(){
      // If the evaluation is requested, query for participations stats
      var evalStats = (await ProjectEvaluationStatsResource.get({id: this.project.id})).body

      this.evalStats = {
        statN : evalStats.statN,
        statPhases: evalStats.statPhases.split(';').map(parseFloat)
      }
    },

    async exportCSV(){
      let data = (await this.$http.get(this.exportLink)).bodyText

      var file = new Blob([data], {type: "text/plain"});
      var filename = this.project.name + " export.csv"

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
  }
};
</script>
