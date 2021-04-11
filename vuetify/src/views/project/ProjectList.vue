<template>
  <v-layout row wrap align-content-start>
    <!-- Title and know more -->
    <v-flex xs12>
      <v-layout>
        <v-flex grow>
          <h1>
            {{ $t('noums.projects') }}
          </h1>
        </v-flex>

        <v-flex shrink class="hidden-xs-only">
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
              {{ $t('pages.projectList.introTitle') }}
            </div>
          </template>
          <v-card class="px-3 py-2">
            <vue-markdown>{{ $t('pages.projectList.introText') }}</vue-markdown>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-flex>

    <!-- Search box -->
    <v-flex xs12>
      <v-card>
        <v-card-text>
          <h3>{{ $t('actions.search') }}</h3>
          <v-layout wrap>
            <v-flex xs12 sm6 md4>
              <v-select v-model="filters.knowledge_area"
                        :label="$t('forms.fields.knowledgeArea')"
                        :items="$store.getters['knowledgearea/all']"
                        :item-text="(i => $t(i.name))"
                        item-value="id"
                        clearable
                        single-line hide-details
                        @change="updateFilter"
              />
            </v-flex>

            <v-flex xs12 sm6 md4>
              <v-select v-model="filters.project_type"
                        :label="$t('forms.fields.projectType')"
                        :items="$store.getters['project/projectTypes'].slice(1)"
                        :item-text="(i => $t(i.name))"
                        item-value="value"
                        clearable
                        single-line hide-details
                        @change="updateFilter"
              />
            </v-flex>

            <v-flex xs12 sm6 md4>
              <v-combobox v-model="filters.country_code"
                          :label="$t('forms.fields.projectCountry')"
                          :items="countries"
                          :item-text="countryTl"
                          clearable
                          single-line hide-details
                          @change="updateFilter"
              />
            </v-flex>
            
            <v-flex xs12>
              <v-combobox v-model="filters.collaboration__structure"
                          :label="$t('forms.fields.structureName')"
                          :items="$store.getters['structure/all']"
                          item-text="name"
                          clearable
                          single-line hide-details
                          @change="updateFilter"
              />
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 class="hidden-sm-and-down">
      <ProjectGrid :show-evaluations="showEvaluations" :projects="projects" />
    </v-flex>

    <v-flex xs12 class="hidden-md-and-up">
      <v-card>
        <ModelList :objects="projects" show-last-modified="true" />
      </v-card>
    </v-flex>

    <!-- Load more buttons -->
    <v-flex xs12 mt-3>
      <v-layout justify-center>
        <v-flex shrink>
          <v-btn
            v-if="canLoadMore || loadMoreDisabled"
            :loading="loadMoreDisabled"
            :disabled="loadMoreDisabled"
            color="primary"
            @click="loadMoreProjects"
          >
            {{ $t('pages.projectList.showMore') }}
          </v-btn>

          <v-btn v-else disabled>
            {{ $t('pages.projectList.noMoreProjects') }}
          </v-btn>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>


<script>
import ProjectGrid from "@/components/project/ProjectGrid";
import ModelList from "@/components/generic/ModelList";

import { slug2id } from "@/plugins/utils";
import { debounce } from "lodash";
import { Countries } from "@/plugins/i18n";


export default {

  metaInfo() {
    return {
      title: this.$t('noums.projects')
    };
  },

  components: {
    ProjectGrid,
    ModelList
  },

  data() {
    return {
      countries: Countries,
      
      showEvaluations: false,

      filters : {},

      projectPage: 0,
      projectPagesize: 12,
      canLoadMore: false,
      loadMoreDisabled: false,
    };
  },

  computed: {
    projects() {
      let list = this.$store.getters["project/all"].slice();
      list.sort((a,b) => b.modified_at.localeCompare(a.modified_at))
      return list
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
    // Data we need
    this.$store.dispatch("knowledgearea/load")
    this.$store.dispatch("structure/load")

    // debouncer
    this.updateFilter = debounce(this.updateFilter, 250);

    // Get URL parameters
    let queryParams = this.$route.query;
    if(queryParams.country_code){
      this.filters.country_code = this.countries.filter(c => c.alpha3Code == queryParams.country_code)[0]
    }
  
    // Load page 0
    this.$store.dispatch('project/clear')
    await this.loadProjectPage();
  },
  
  methods: {
    async loadProjectPage(){
      let filters = this.filters;

      let params = {
        offset: this.projectPage * this.projectPagesize,
        limit: this.projectPagesize
      }

      // TODO: multivalued filters?

      params = {
        ...params,
        ...filters,
        ordering:"-modified_at",
      }

      if(params.collaboration__structure)
        params.collaboration__structure = params.collaboration__structure.id

      if(params.country_code)
        params.country_code = params.country_code.alpha3Code

      // Enable or disable "load more" button here
      let countBefore = this.$store.getters['project/all'].length

      await this.$store.dispatch("project/load", { params })

      let countAfter = this.$store.getters['project/all'].length
      this.canLoadMore = countAfter - countBefore == this.projectPagesize

      // special check on page 1
      if(this.projectPage == 0)
        this.canLoadMore = countAfter == this.projectPagesize;
    },

    async loadMoreProjects(){
      this.loadMoreDisabled = true;
      // Load next batch
      this.projectPage += 1;
      await this.loadProjectPage();
      // Increase page
      this.loadMoreDisabled = false;
    },

    async updateFilter(){
      this.$store.dispatch('project/clear');
      this.showEvaluations = false;
      this.projectPage = 0;
      this.loadProjectPage();
    },

    countryTl(country){
      let lang = this.$i18n.locale
      if(country.translations.hasOwnProperty(lang)){
        return country.translations[lang]
      }
      return country.name
    },
  },

};
</script>

