<style scoped>
  th{
    text-align: left;
    padding-right: 8px;
    padding-bottom: 4px;
  }
  .gray-hover:hover{
    background-color: #F8F8F8
  }
</style>


<template>
  <v-layout v-if="user" row wrap align-content-start>
    <v-flex xs12>
      <h1> {{ user.full_name }} | {{ $t('pages.account.title') }}</h1>
    </v-flex>

    <v-flex v-if="$route.query.welcome" xs12>
      <v-alert color="success" :value="true" class="subheading">
        <v-icon dark>
          check
        </v-icon>&nbsp;
        {{ $t('pages.account.accountCreated') }}
      </v-alert>
    </v-flex>

    <!-- Account Details -->
    <v-flex xs12>
      <v-card flat>
        <v-card-text v-if="!showEditForm">
          <v-layout row wrap justify-center>
            <v-flex shrink px-5>
              <v-img width="130" :src="user.avatar_url" />
              <br>
              <table width="100%">
                <tr>
                  <th>{{ $t('forms.fields.username') }}</th>
                  <td>{{ user.username }}</td>
                </tr>
                <tr>
                  <th>{{ $t('noums.projects') }}</th>
                  <td>{{ projectIds.length }} {{ $t('noums.projects') | lowercase }}</td>
                </tr>
                <tr>
                  <th>{{ $t('noums.structures') }}</th>
                  <td>{{ structureIds.length }} {{ $t('noums.structures') | lowercase }}</td>
                </tr>
              </table>
            </v-flex>
            <v-flex grow>
              <table width="100%">
                <tr>
                  <th>{{ $t('forms.fields.firstName') }}</th>
                  <td>{{ user.first_name }}</td>
                </tr>
                <tr>
                  <th>{{ $t('forms.fields.lastName') }}</th>
                  <td>{{ user.last_name }}</td>
                </tr>
                <tr>
                  <th>{{ $t('forms.fields.education') }}</th>
                  <td v-if="user.education_level">
                    {{ $t(`models.educationLevel.${user.education_level.toLowerCase()}`) }}
                  </td>
                  <td v-else>
                    {{ $t('misc.notSpecified') }}
                  </td>
                </tr>
                <tr>
                  <th>{{ $t('forms.fields.institution') }}</th>
                  <td>{{ user.institution || $t('misc.notSpecified') }}</td>
                </tr>
                <tr>
                  <th>{{ $t('forms.fields.genderIdentity') }}</th>
                  <td v-if="user.gender">{{ $t(`models.userGender.${user.gender.toLowerCase()}`) }}</td>
                  <td v-else>{{ $t('misc.notSpecified') }}</td>
                </tr>
              </table>
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-text v-else>
          <v-form ref="profileEditForm" v-model="editProfileValid" @submit.prevent="submitUpdateProfile()">
            <v-layout pt-3 row wrap>
              <!-- Edit Profile Form -->

              <v-flex xs12>
                <b>Avatar Image:</b> To change your avatar image go to <a href="https://en.gravatar.com/">
                  Gravatar
                </a> and create a new account with the email provided for the platform.
              </v-flex>

              <v-flex xs12>
                <v-checkbox
                  v-model="editUser.hide_realname"
                  :label="$t('forms.fields.isAnonymous')"
                  :hint="$t('forms.hints.isAnonymous')"
                  persistent-hint
                />
              </v-flex>

              <v-flex xs12 sm6 py-0>
                <v-text-field
                  v-model="editUser.first_name"
                  :rules="[rules.required]"
                  :label="$t('forms.fields.firstName')"
                />
              </v-flex>
              <v-flex xs12 sm6 py-0>
                <v-text-field
                  v-model="editUser.last_name"
                  :rules="[rules.required]"
                  :label="$t('forms.fields.lastName')"
                />
              </v-flex>
              <v-flex xs12 py-0>
                <v-select
                  v-model="editUser.gender"
                  :item-text="e => $t(e.name)"
                  :items="$store.getters['user/genders']"
                  :label="$t('forms.fields.genderIdentity')"
                />
              </v-flex>
              <v-flex xs12 py-0>
                <v-select
                  v-model="editUser.education_level"
                  :item-text="e => $t(e.name)"
                  :items="$store.getters['user/educationLevels']"
                  :label="$t('forms.fields.education')"
                />
              </v-flex>
              <v-flex xs12 py-0>
                <v-text-field
                  v-model="editUser.institution"
                  :label="$t('forms.fields.institution')"
                />
              </v-flex>

            <!-- /Edit Profile Form -->
            </v-layout>
            <input type="submit" style="display:none">
          </v-form>
        </v-card-text>

        <v-card-actions v-if="isOwnUser" class="px-3 pb-3">
          <v-spacer />
          <v-btn v-if="showEditForm" color="success" class="elevation-0"
                 @click="submitUpdateProfile()"
          >
            {{ $t('pages.account.saveProfile') }}
          </v-btn>
          <v-btn v-else outline color="warning" class="elevation-0" @click="showEditForm = true">
            <v-icon left>edit</v-icon>
            {{ $t('pages.account.editProfile') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

    <!-- Evaluation requests list -->
    <v-flex v-if="isOwnUser && currentUser.evaluations" xs12>
      <v-card flat>
        <v-card-title>
          <h2 class="title">
            {{ $t('pages.account.evaluationRequests') }}
          </h2>
        </v-card-title>
        <v-card-text>
          <v-sheet :max-height="300" style="overflow-y:auto; overflow-x:hidden">
            <v-list two-line>
              <template v-for="(evaluation, idx) in sortEvals(currentUser.evaluations)">
                <v-divider v-if="idx != 0" :key="idx+'-divider'" />
              
                <v-list-tile :key="evaluation.id">
                  <v-list-tile-avatar tile size="60" class="ma-0 pa-0 mr-3">
                    <v-img :src="project(evaluation.project).image_url" ratio="1" />
                  </v-list-tile-avatar>

                  <v-list-tile-content>
                    <v-list-tile-title>
                      <strong>
                        {{ project(evaluation.project).name }}
                      </strong>
                    </v-list-tile-title>
                    <v-list-tile-sub-title>
                      {{ $t(`models.projectPhase.phase${evaluation.project_phase}`) }}
                    </v-list-tile-sub-title>
                  </v-list-tile-content>

                  <v-list-tile-action>
                    <v-btn
                      color="success"
                      class="elevation-0 px-2"
                      :outline="!evaluation.is_complete"
                      :to="{name:'evaluation-entry', params:{slug: evaluation.id }}"
                    >
                      {{ $t('pages.projectManage.evalViewEvaluation') }}
                      &nbsp; <span v-if="evaluation.is_complete">{{ $t('pages.projectManage.evalComplete') }}</span>
                    </v-btn>
                  </v-list-tile-action>
                </v-list-tile>
              </template>
            </v-list>
          </v-sheet>
        </v-card-text>
      </v-card>
    </v-flex>

    <!-- Project and Structures -->
    <v-flex xs12>
      <v-layout row wrap>
        <!-- Own projects -->
        <v-flex xs12 sm6>
          <h2 class="mb-3">
            {{ $t('pages.account.myProjects') }}
          </h2>

          <v-card flat>
            <v-card-text>
              <v-btn v-if="isOwnUser" fab small absolute top
                     right
                     dark
                     style="margin-right:60px"
                     :title="$t('actions.exportAllData')"
                     @click="exportProjectsCSV()"
              >
                <v-icon>mdi-database-export</v-icon>
              </v-btn>
              <v-btn v-if="isOwnUser" fab small absolute top
                     right
                     color="success"
                     :title="$t('pages.projectCreate.title')"
                     :to="{name:'project-create'}"
              >
                <v-icon>add</v-icon>
              </v-btn>

              <ModelList :objects="projects" show-last-modified="true" />

              <!-- <template v-for="(project,idx) in projects">
                <v-card
                  :key="project.id"
                  class="gray-hover"
                  flat
                  :to="project.link"
                >
                  <v-img v-if="project.image_url" :src="project.image_url" :height="idx==0 ? '125' : '50'" />
                  <v-card-text class="px-0">
                    <b>{{ project.name }}</b><br>
                    {{ project.summary | ellipsis(100) }}
                  </v-card-text>
                </v-card>
                <v-divider :key="idx+'-div'" class="mb-3" />
              </template> -->
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Own structures -->
        <v-flex v-if="structures" xs12 sm6>
          <h2 class="mb-3">
            {{ $t('pages.account.myStructures') }}
          </h2>

          <v-card flat>
            <v-card-text>
              <v-btn v-if="isOwnUser" fab small absolute top
                     right
                     dark
                     style="margin-right:60px"
                     :title="$t('actions.exportAllData')"
                     @click="exportStructuresCSV()"
              >
                <v-icon>mdi-database-export</v-icon>
              </v-btn>
              <v-btn v-if="isOwnUser" fab small absolute top
                     right
                     color="success"
                     :title="$t('pages.structureCreate.title')"
                     :to="{name:'structure-create'}"
              >
                <v-icon>add</v-icon>
              </v-btn>

              <ModelList :objects="structures" show-last-modified="true" big-images="true" />

              <!-- <template v-for="(structure,idx) in structures">
                <v-card
                  :key="structure.id"
                  class="gray-hover"
                  flat
                  :to="structure.link"
                >
                  <v-img v-if="structure.image_url" :src="structure.image_url" :height="idx==0 ? '125' : '50'" />
                  <v-card-text class="px-0">
                    <b>{{ structure.name }}</b><br>
                    {{ structure.summary | ellipsis(100) }}
                  </v-card-text>
                </v-card>
                <v-divider :key="idx+'-div'" class="mb-3" />
              </template> -->
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import ModelList from "@/components/generic/ModelList";

import { onlyUnique, slug2id, donwloadAsyncCSV } from "@/plugins/utils";
import { API_SERVER } from "@/plugins/resource";
import { cloneDeep } from "lodash";

export default {

  components: {
    ModelList,
  },

  metaInfo(){
    return {
      title: this.$t("pages.account.title")
    }
  },

  data(){
    return{
      editUser: {},
      editProfileValid: null,
      showEditForm: false,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
    }
  },

  computed:{
    userId(){
      let slug = this.$route.params.slug
      if (slug){ return slug2id(slug) }

      let loggedInUser = this.$store.getters['user/current']
      if(loggedInUser.id > 0){ return loggedInUser.id }

      return null
    },

    /** Current User being displayed */
    user(){
      return this.$store.getters["user/detail"](this.userId)
    },

    /** Projects the user has */
    projects(){
      let projects = this.projectIds.map(id => this.$store.getters['project/detail'](id))
      projects = projects.filter(i => i.modified_at != null)
      projects.sort((a,b) => b.modified_at.localeCompare(a.modified_at))

      return projects
    },

    /** Structures the user participates in */
    structures(){
      let structures = this.structureIds.map(id => this.$store.getters['structure/detail'](id))
      structures = structures.filter(i => i.modified_at != null)
      structures.sort((a,b) => b.modified_at.localeCompare(a.modified_at))

      return structures
    },

    isOwnUser(){
      return this.userId == this.$store.getters['user/current'].id
    },

    currentUser(){
      return this.$store.getters['user/current']
    },

    projectIds(){
      let pids = [
        ...this.user.owned_projects,
        ...this.user.managed_projects,
        ...this.user.researched_projects,
      ]
      return pids.filter(onlyUnique)
    },

    structureIds(){
      let pids = [
        ...this.user.managed_structures,
        ...this.user.owned_structures,
      ]
      return pids.filter(onlyUnique)
    },

  },

  async created(){
    await this.$store.dispatch("user/load", [this.userId])
    this.editUser = cloneDeep(this.$store.getters['user/current'])

    if(this.userId == null){
      console.error("Account.vue: No logged in user or request.")
      this.$router.push({name:"home"})
    }

    if(this.isOwnUser){
      this.$store.dispatch('user/loadCurrentEvaluations')
    }

    await Promise.all([
      this.$store.dispatch("project/load", this.projectIds),
      this.$store.dispatch("structure/load", this.structureIds)
    ])
  },

  methods:{

    project(id){
      return this.$store.getters['project/detail'](id);
    },

    structure(id){
      return this.$store.getters['structure/detail'](id);
    },

    sortEvals(evals){
      evals = evals.slice()
      // Sort by incomplete first.
      evals.sort((a,b) => (a.is_complete ? 1:0) - (b.is_complete ? 1:0));
      return evals;
    },

    async exportProjectsCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/all_own_projects.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_own_projects.csv');
    },

    async exportStructuresCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/all_own_structures.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_own_structures.csv');
    },

    async submitUpdateProfile(){
      try{
        await this.$store.dispatch('user/updateCurrent', this.editUser)
        await this.$store.dispatch("toast/success", this.$t('pages.account.updateProfileSuccess'))

        await this.$store.dispatch("user/load")
        await this.$store.dispatch("user/load", [this.userId])
        this.editUser = cloneDeep(this.$store.getters['user/current'])

        this.showEditForm = false;
      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t('pages.account.updateProfileFailure'),
          error
        })
      }
    }

  }

};
</script>
