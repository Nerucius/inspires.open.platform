<style scoped>
th{
  text-align: right;
  padding-right: 8px;
}
.gray-hover:hover{
  background-color: #F8F8F8
}
</style>


<template>
  <v-layout v-if="user" row wrap align-content-start>
    <v-flex xs12>
      <h1>Account Dashboard</h1>
    </v-flex>

    <v-flex v-if="$route.query.newUser" xs12>
      <v-alert color="success" :value="true" class="subheading">
        <v-icon dark>
          check
        </v-icon>&nbsp;
        Your new account has been created successfully. You can now access all of the features of the platform.
      </v-alert>
    </v-flex>

    <!-- Account Details -->
    <v-flex xs12 pb-0>
      <h2>Details</h2>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text v-if="!showEditForm">
          <table style="max-width:400px">
            <tr>
              <th>First Name</th>
              <td>{{ user.first_name }}</td>
            </tr>
            <tr>
              <th>Last Name</th>
              <td>{{ user.last_name }}</td>
            </tr>
            <tr>
              <th>Email</th>
              <td>{{ user.email }}</td>
            </tr>
          </table>
        </v-card-text>
        <v-card-text v-else>
          <v-form ref="showEditForm">
            <v-layout pt-3 row wrap>
              <!-- Edit Profile Form -->

              <v-flex xs12 sm6 py-0>
                <v-text-field
                  v-model="editUser.first_name"
                  box
                  :rules="[rules.required]"
                  :label="$t('forms.fields.firstName')"
                />
              </v-flex>
              <v-flex xs12 sm6 py-0>
                <v-text-field
                  v-model="editUser.last_name"
                  box
                  :rules="[rules.required]"
                  :label="$t('forms.fields.lastName')"
                />
              </v-flex>
              <v-flex xs12 py-0>
                <v-text-field
                  v-model="editUser.email"
                  box
                  :rules="[rules.required]"
                  :label="$t('forms.fields.email')"
                />
              </v-flex>

            <!-- /Edit Profile Form -->
            </v-layout>
          </v-form>
        </v-card-text>
        <v-card-actions class="px-3">
          <v-spacer />
          <!-- <v-btn v-if="showEditForm" flat @click="showEditForm = !showEditForm">
            Save Profile
          </v-btn>
          <v-btn v-else flat @click="showEditForm = !showEditForm">
            Edit Profile
          </v-btn> -->
        </v-card-actions>
      </v-card>
    </v-flex>


    <!-- Last 3 Cards -->
    <v-flex xs12 pb-0>
      <h2>Latest Updates</h2>
    </v-flex>

    <v-flex xs12>
      <v-layout row wrap>
        <v-flex xs12 sm6 md4>
          <v-card flat>
            <v-card-text>
              <v-btn v-if="isOwnUser" fab small absolute top
                     right
                     title="Create new Project"
                     color="success"
                     :to="{name:'project-create'}"
              >
                <v-icon>add</v-icon>
              </v-btn>

              <h3 class="mb-2">
                Projects
              </h3>

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

        <v-flex xs12 sm6 md4>
          <v-card flat>
            <v-card-text>
              <v-btn v-if="isOwnUser" fab small absolute top
                     right
                     title="Create new Structure"
                     color="success"
                     :to="{name:'structure-create'}"
              >
                <v-icon>add</v-icon>
              </v-btn>

              <h3 class="mb-2">
                Structures
              </h3>

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

        <v-flex xs12 sm6 md4>
          <v-card flat>
            <v-card-title>
              <h3>Commissioners</h3>
            </v-card-title>
          </v-card>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { onlyUnique, slug2id } from "@/plugins/utils";
import { cloneDeep } from "lodash";

export default {

  data(){
    return{
      editUser: null,
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
  }

};
</script>
