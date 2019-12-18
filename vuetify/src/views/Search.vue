<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.search.searchResultsFor', {term}) }}</h1>
      <h3>
        {{ $t('pages.search.searchFound', {number:searchResultsCount}) }}
      </h3>

    </v-flex>

    <v-flex xs12>
      <v-layout row wrap>
        <v-flex v-for="object in searchResults" :key="object._type+object.id" xs12 sm6 md4 lg3 xl2 mb-3>
          <v-card flat dark>
            <v-card-title class="px-3 py-1 text-uppercase">
              <span v-if="object._type=='Project'">{{ $t('noums.project') }}</span>
              <span v-if="object._type=='Structure'">{{ $t('noums.structure') }}</span>
            </v-card-title>
          </v-card>
          <StructureCard v-if="object._type=='Structure'" :structure="object" />
          <ProjectCard v-if="object._type=='Project'" :project="object" />
        </v-flex>
      </v-layout>
    </v-flex>

  </v-layout>
</template>


<script>
import StructureCard from "@/components/structure/StructureCard";
import ProjectCard from "@/components/project/ProjectCard";

import {SearchResource} from "@/plugins/resource"
import { createLink as createLinkProject } from "@/store/Project"
import { createLink as createLinkStructure } from "@/store/Structure"

export default {

  metaInfo(){
    return {
      title: this.$t("pages.search.title")
    }
  },

  data() {
    return {
      searchResults : [],
      searchResultsCount : 0,
    }
  },

  components: {
    StructureCard,
    ProjectCard
  },

  computed: {
    term(){
      return this.$route.query['q']
    }
  },

  created() {
    this.search(this.term);
  },

  methods: {
    async search(term){
      // Get search results
      let response = await SearchResource.get({term})

      this.searchResultsCount = response.body.count
      this.searchResults = response.body.data.map(item => {
        if (item._type == 'Project') return createLinkProject(item);
        if (item._type == 'Structure') return createLinkStructure(item);
        return item;
      });
    }
  },

}
</script>
