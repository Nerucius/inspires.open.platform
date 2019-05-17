<template>
  <v-layout row wrap align-content-start>

    <v-flex xs12>
      <h1 class="mb-3">
        {{ $t('noums.projects') }}
        <small v-if="filterKnowledgeArea">
          | {{ $t('pages.projectList.filterByArea', {area:$t(filterKnowledgeArea.name)}) }}
        </small>
      </h1>

      <v-expansion-panel>
        <v-expansion-panel-content>
          <template v-slot:header>
            <div class="subheading">Want to know more about projects?</div>
          </template>
          <v-card class="px-3 py-2">
            <vue-markdown>{{ $t('pages.projectList.introText') }}</vue-markdown>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>


    </v-flex>

    <v-flex xs12>
      <ProjectGrid hide-title="true" :projects="projects" />
    </v-flex>
  </v-layout>
</template>


<script>
import ProjectGrid from "@/components/project/ProjectGrid";
import { slug2id } from "@/plugins/utils";


export default {

  metaInfo() {
    return {
      title: this.$t('noums.projects')
    };
  },

  components: {
    ProjectGrid
  },

  data() {
    return {};
  },

  computed: {
    projects() {
      return this.$store.getters["project/all"];
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
      await this.$store.dispatch("project/load", {params:{limit:20, knowledge_area}})
    }else{
      await this.$store.dispatch("project/load", {params:{limit:20}})
    }
  }
};
</script>

