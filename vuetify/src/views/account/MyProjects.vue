<template>
  <v-layout row wrap align-content-start>
    <v-flex xs6>
      <h1>My Projects</h1>
    </v-flex>
    <v-flex xs6 class="text-xs-right">
      <v-btn color="success"
             :to="{name:'project-create'}"
      >
        Create a New Project
      </v-btn>
    </v-flex>


    <v-flex v-for="project in projects" :key="project.id" xs12>
      <v-card class="mb-3 py-3">
        <v-layout row>
          <v-flex xs2 class="text-xs-center">
            <v-btn
              v-if="isManager(project)" fab small
              title="You are a manager"
              color="warning" class="elevation-0"
            >
              {{ "Manager" | ellipsis(1, false) }}
            </v-btn>
            <v-btn
              v-if="isResearcher(project)" fab small
              title="You are a researcher"
              color="success" class="elevation-0"
            >
              {{ "Researcher" | ellipsis(1, false) }}
            </v-btn>
          </v-flex>
          <v-flex pr-4>
            <h3>{{ project.name }}</h3>
            <p>
              {{ project.summary }}
            </p>
            <p class="text-xs-right">
              <v-btn
                v-if="isManager(project)"
                :to="{name:'project-manage', params:{slug:obj2slug(project)}}"
                outline color="warning"
              >
                Manage
              </v-btn>
              <v-btn
                :to="{name:'project-detail', params:{slug:obj2slug(project)}}"
                outline color="success"
              >
                View
              </v-btn>
            </p>
          </v-flex>
        </v-layout>
      </v-card>
    </v-flex>
  </v-layout>
</template>


<script>
import { onlyUnique, obj2slug } from "@/plugins/utils";

export default {
  data(){
    return {
      obj2slug
    }
  },

  computed:{
    projects(){
      let detail = this.$store.getters["project/detail"]
      return this.projectIds.map(pid => detail(pid)).filter(e => !!e.id)
    },

    projectIds(){
      let pids = [
        ...this.$store.getters['user/current'].owned_projects,
        ...this.$store.getters['user/current'].managed_projects,
        ...this.$store.getters['user/current'].researched_projects,
      ]
      return pids.filter(onlyUnique)
    }
  },

  async mounted(){
    await this.$store.dispatch("user/load")
    this.$store.dispatch("project/load", this.projectIds)
  },

  methods:{
    isResearcher(project){
      let userId = this.$store.getters['user/current'].id
      return project.researchers.indexOf(userId) >= 0
    },
    isManager(project){
      let userId = this.$store.getters['user/current'].id
      return project.managers.indexOf(userId) >= 0 || project.owner == userId
    }
  }
}
</script>
