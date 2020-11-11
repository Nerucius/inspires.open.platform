<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <v-layout>
        <v-flex grow>
          <h1>
            {{ $t('noums.projects') }}
            <small v-if="filterKnowledgeArea">
              | {{ $t('pages.projectList.filterByArea', {area:$t(filterKnowledgeArea.name)}) }}
            </small>
          </h1>
        </v-flex>

        <v-flex shrink>
          <v-switch v-model="showEvaluations"
                    color="primary"
                    class="mt-0 pa-0"
                    :label="$t('pages.projectList.showEvaluations')"
          />
        </v-flex>
      </v-layout>

      <v-expansion-panel>
        <v-expansion-panel-content>
          <template v-slot:header>
            <div class="subheading">
              Want to know more about projects?
            </div>
          </template>
          <v-card class="px-3 py-2">
            <vue-markdown>{{ $t('pages.projectList.introText') }}</vue-markdown>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-flex>

    <v-flex xs12>
      <v-layout row wrap align-content-start>
        <v-flex v-for="project in projects" :key="project.id" xs12 sm6 md4 lg3 xl2 mb-3>
          <ProjectCard :show-evaluation="showEvaluations" :project="project" />
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>


<script>
import ProjectCard from "@/components/project/ProjectCard";
import { slug2id } from "@/plugins/utils";


export default {

  metaInfo() {
    return {
      title: this.$t('noums.projects')
    };
  },

  components: {
    ProjectCard
  },

  data() {
    return {
      showEvaluations: false,
    };
  },

  computed: {
    projects() {
      let projectList = this.$store.getters["project/all"].slice();
        projectList.sort( (a,b) => {
        return a.name.localeCompare(b.name)
      })
      return projectList;
    },

    filterKnowledgeArea(){
      let areaSlug = this.$route.params.area
      if(areaSlug){
        let areaId = slug2id(areaSlug)
        return this.$store.getters["knowledgearea/get"](areaId)
      }
      return null
    }
  },

  async created(){
    await this.$store.dispatch("knowledgearea/load")

    if (this.filterKnowledgeArea){
      let knowledge_area = this.filterKnowledgeArea.id
      this.$store.dispatch("project/clear")
      // await this.$store.dispatch("project/load", {params:{limit:20, knowledge_area}})
      await this.$store.dispatch("project/load", {params:{knowledge_area}})
    }else{
      // await this.$store.dispatch("project/load", {params:{limit:20}})
      await this.$store.dispatch("project/load")
    }
  }
};
</script>

