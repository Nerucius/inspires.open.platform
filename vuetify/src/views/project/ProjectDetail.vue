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
              <v-list-tile-sub-title>{{ $t('noums.structure') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Country -->
          <v-list-tile v-if="project.country_code" :to="structure.link">
            <v-list-tile-avatar tile>
              <flag style="font-size:40px" :squared="false" :iso="iso3toiso2(project.country_code)"></flag>
              <!-- <v-img :src="structure.image_url" /> -->
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ countryTranslation(project.country_code) }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.projectCountry') }}</v-list-tile-sub-title>
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

          <v-toolbar dense flat color="primary" dark class="mt-3">
            <h1 class="title">
              {{ $t('forms.fields.participants') }}
            </h1>
          </v-toolbar>

          <v-sheet :max-height="72*4.5" style="overflow-y:auto;">
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


    <v-flex xs12 sm8>
      <v-img :src="project.image_url" height="200">
        <v-toolbar flat style="background-color:rgba(0,0,0,.3)" dark>
          <h1 class="title">
            {{ project.name }}
          </h1>
        </v-toolbar>
      </v-img>


      <v-tabs v-model="page.tab" grow>
        <v-tabs-slider color="primary" />
        <v-tab v-for="item in page.items" :key="item">
          {{ $t(item) }}
        </v-tab>
      </v-tabs>

      <!-- Main Body -->
      <v-tabs-items v-model="page.tab">
        <!-- TAB: Project Details -->
        <v-tab-item key="pages.projectDetail.detailsTab">
          <v-card flat>
            <div class="py-1 px-3 text-xs-right">
              <small>
                {{ $t('misc.lastUpdated', {time: moment(project.modified_at).fromNow()}) }}
              </small>
            </div>
            <div class="px-4 pt-4 pb-2 grey lighten-4 subheading" style="font-spacing:110%">
              <vue-markdown>{{ project.summary }}</vue-markdown>
            </div>

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

              <div v-if="isParticipant" class="my-4 text-xs-center">
                <v-btn large dark
                       :to="{...project.link, name:'evaluation-detail'}"
                       class="elevation-0"
                >
                  <v-icon left>
                    mdi-school
                  </v-icon>
                  View detailed evaluation for participants
                </v-btn>
              </div>

              <template v-if="isParticipant">
                <p>{{ $t('pages.evaluationEntry.selfQuestionnaireDescription') }}</p>

                <p class="text-xs-center">
                  <v-btn large dark color="red" href="https://app.inspiresproject.com/uploads/inspires-self-questionaire.pdf" target="_blank">
                    <v-icon left>
                      mdi-file-pdf
                    </v-icon>
                    {{ $t('actions.downloadName', {name: $t('pages.evaluationEntry.selfQuestionnaireTitle')}) }}
                  </v-btn>
                </p>
              </template>


              <div class="pa-3 text-xs-center">
                <h3 class="display-1">
                  {{ project.name }}
                </h3>

                <v-sheet height="600">
                  <ProjectTangram :project="project">
                    <div class="subheading py-4">
                      {{ $t('pages.projectDetail.projectNotYetEvaluated') }}
                    </div>
                  </ProjectTangram>
                </v-sheet>
              </div>

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
import ProjectCardHorizontal from "@/components/project/ProjectCardHorizontal";
import ProjectTangram from "@/components/evaluation/ProjectTangram";
import { API_SERVER } from "@/plugins/resource";


export default {
  metaInfo() {
    return {
      title: (this.project || {}).name
    };
  },

  components: {
    ProjectCardHorizontal,
    ProjectTangram,
  },

  data() {
    return {
      moment,
      obj2slug,
      iso3toiso2,
      project: null,
      structure: null,
      page:{
        tab: null,
        items:[
          'pages.projectDetail.detailsTab',
          'pages.projectDetail.evaluationTab',
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
      this.$store.dispatch("project/load");
      await this.$store.dispatch("project/load", [this.projectId]);
      this.project = this.$store.getters["project/detail"](this.projectId);

      // If project has a collaboration, load structure
      if(this.project.collaboration){
        let structureId = this.project.collaboration.structure
        await this.$store.dispatch("structure/load", [structureId]);
        this.structure = this.$store.getters['structure/detail'](structureId)
      }


    } catch (error) {
      this.$store.dispatch('toast/error', {
        message:this.$t('pages.projectDetail.projectNotFound'),
        error
      })
    }
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
