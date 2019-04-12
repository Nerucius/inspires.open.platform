<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1 class="mb-2">
        {{ $t('noums.projects') }}
        <small v-if="filterKnowledgeArea">
          {{ $t('pages.projectList.filterByArea', {area:$t(filterKnowledgeArea.name)}) }}
        </small>
      </h1>
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
      title: "All Projects"
    }
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

  mounted: async function(){
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

