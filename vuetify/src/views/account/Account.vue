<style scoped>
th{
  text-align: right;
  padding-right: 8px;
}
</style>


<template>

  <v-layout row wrap align-content-start>

    <v-flex xs12>
      <h1>Account Dashboard</h1>
    </v-flex>

    <v-flex xs12 pb-0>
      <h2>Details</h2>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <table style="max-width:400px">
            <tr>
              <th>First Name</th>
              <td>{{current.first_name}}</td>
            </tr>
            <tr>
              <th>Last Name</th>
              <td>{{current.last_name}}</td>
            </tr>
            <tr>
              <th>Email</th>
              <td>{{current.email}}</td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </v-flex>


    <!-- Last 3 Cards -->
    <v-flex xs12 pb-0>
      <h2>Latest Updates</h2>
    </v-flex>
    <v-flex xs12>
        <v-layout row wrap>
          <v-flex sm6 md4>
            <v-card flat>
              <v-card-text>
                <h3>Projects</h3>
                <v-list three-line>
                  <v-list-tile
                    v-for="(project, idx) in projects"
                    :to="{name:'project-detail', params:{slug:obj2slug(project)}}"
                    :key="project.id">
                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{project.name}}
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{project.summary}}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>
                  </v-list-tile>
                </v-list>
              </v-card-text>
            </v-card>
          </v-flex>
          <v-flex sm6 md4>
            <v-card flat>
              <v-card-title>
                <h3>Structures</h3>
              </v-card-title>
            </v-card>
          </v-flex>
          <v-flex sm6 md4>
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

export default {

  data(){
    return{
      obj2slug
    }
  },

  mounted(){
    this.$store.dispatch("project/load", this.projectIds)
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
    }
  }

};
</script>
