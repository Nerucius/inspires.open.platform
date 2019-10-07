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
          <v-layout row wrap>
            <v-flex xs12 sm6>
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
              </table>
            </v-flex>
            <v-flex xs12 sm6>
              <table width="100%">
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
          </v-layout>
        </v-card-text>

        <v-card-text v-else>
          <v-form ref="profileEditForm" v-model="editProfileValid">
            <v-layout pt-3 row wrap>
              <!-- Edit Profile Form -->

              <v-flex xs12>
                <b>Avatar Image:</b> To change your avatar image go to <a href="https://en.gravatar.com/">
                  Gravatar
                </a> and create a new account with the email provided for the platform.
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
          </v-form>
        </v-card-text>

        <v-card-actions v-if="isOwnUser" class="px-3 pb-3">
          <v-spacer />
          <v-btn v-if="showEditForm" color="success" class="elevation-0"
                 @click="submitUpdateProfile()"
          >
            {{ $t('pages.account.saveProfile') }}
          </v-btn>
          <v-btn v-else color="success" class="elevation-0" @click="showEditForm = true">
            {{ $t('pages.account.editProfile') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>


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

              <template v-for="(project,idx) in projects">
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
              </template>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Own structures -->
        <v-flex xs12 sm6>
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

              <template v-for="(structure,idx) in structures">
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
              </template>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- <v-flex xs12 sm6 md4>
          <v-card flat>
            <v-card-title>
              <h3>Commissioners</h3>
            </v-card-title>
          </v-card>
        </v-flex> -->
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { onlyUnique, slug2id, donwloadAsyncCSV } from "@/plugins/utils";
import { API_SERVER } from "@/plugins/resource";
import { cloneDeep } from "lodash";

export default {

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
      return this.projectIds.map(id => this.$store.getters['project/detail'](id))
    },

    /** Structures the user participates in */
    structures(){
      return this.structureIds.map(id => this.$store.getters['structure/detail'](id))
    },

    isOwnUser(){
      return this.userId == this.$store.getters['user/current'].id
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

  async mounted(){
    await this.$store.dispatch("user/load", [this.userId])
    this.editUser = cloneDeep(this.user)

    if(this.userId == null){
      console.error("Account.vue: No logged in user or request.")
      this.$router.push({name:"home"})
    }

    await this.$store.dispatch("project/load", this.projectIds)
    await this.$store.dispatch("structure/load", this.structureIds)
  },

  methods:{

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

        await this.$store.dispatch("user/load", [this.userId])
        this.editUser = cloneDeep(this.user)

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
