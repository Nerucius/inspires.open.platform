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
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>Account Dashboard</h1>
    </v-flex>

    <v-flex v-if="$route.query.newUser" xs12>
      <v-alert color="success" :value="true">
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
              <td>{{ current.first_name }}</td>
            </tr>
            <tr>
              <th>Last Name</th>
              <td>{{ current.last_name }}</td>
            </tr>
            <tr>
              <th>Email</th>
              <td>{{ current.email }}</td>
            </tr>
          </table>
        </v-card-text>
        <v-card-text v-else>
          <v-form ref="showEditForm">
          <v-layout pt-3 row wrap>
            <!-- Edit Profile Form -->

              <v-flex xs12 sm6 py-0>
                <v-text-field
                  box
                  :rules="[rules.required]"
                  v-model="editUser.first_name"
                  :label="$t('forms.fields.firstName')"
                />
              </v-flex>
              <v-flex xs12 sm6 py-0>
                <v-text-field
                  box
                  :rules="[rules.required]"
                  v-model="editUser.last_name"
                  :label="$t('forms.fields.lastName')"
                />
              </v-flex>
              <v-flex xs12 py-0>
                <v-text-field
                  box
                  :rules="[rules.required]"
                  v-model="editUser.email"
                  :label="$t('forms.fields.email')"
                />
              </v-flex>

            <!-- /Edit Profile Form -->
          </v-layout>
          </v-form>
        </v-card-text>
        <v-card-actions class="px-3">
          <v-spacer></v-spacer>
          <v-btn flat v-if="showEditForm" @click="showEditForm = !showEditForm">
            Save Profile
          </v-btn>
          <v-btn flat v-else @click="showEditForm = !showEditForm">
            Edit Profile
          </v-btn>
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
              <v-btn fab small absolute top right
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
                  :to="{name:'project-detail', params:{slug:obj2slug(project)}}"
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
              <v-btn fab small absolute top right
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
                  :to="{name:'structure-detail', params:{slug:obj2slug(structure)}}"
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
import { onlyUnique, obj2slug } from "@/plugins/utils";
import { cloneDeep } from "lodash";

export default {

  data(){
    return{
      obj2slug,
      editUser: null,
      showEditForm: true,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
    }
  },

  computed:{
    current(){
      return this.$store.getters['user/current']
    },
    projectIds(){
      let pids = [
        ...this.current.owned_projects,
        ...this.current.managed_projects,
        ...this.current.researched_projects,
      ]
      return pids.filter(onlyUnique)
    },
    projects(){
      return this.projectIds.map(id => this.$store.getters['project/detail'](id))
    },
    structureIds(){
      let pids = [
        ...this.current.managed_structures,
        ...this.current.owned_structures,
      ]
      return pids.filter(onlyUnique)
    },
    structures(){
      return this.structureIds.map(id => this.$store.getters['structure/detail'](id))
    },
  },

  async mounted(){
    await this.$store.dispatch("user/loadCurrent")
    this.editUser = cloneDeep(this.current)
    this.$store.dispatch("project/load", this.projectIds)
    this.$store.dispatch("structure/load", this.structureIds)
  }

};
</script>
