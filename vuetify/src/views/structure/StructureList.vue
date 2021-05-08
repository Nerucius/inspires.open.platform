<template>
  <v-layout row wrap align-content-start>
    <!-- Title and intro -->
    <v-flex xs12>
      <h1 class="mb-3">
        {{ $t('noums.structures') }}
      </h1>

      <v-expansion-panel>
        <v-expansion-panel-content>
          <template v-slot:header>
            <div class="subheading">
              {{ $t('pages.structureList.introTitle') }}
            </div>
          </template>
          <v-card class="px-3 py-2">
            <vue-markdown>{{ $t('pages.structureList.introText') }}</vue-markdown>
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
            <!-- Filter Form Fields -->
            <v-flex xs12 sm6>
              <v-select v-model="filters.structure_type"
                        :label="$t('forms.fields.structureType')"
                        :items="$store.getters['structure/structureTypes'].slice(1)"
                        :item-text="(i => $t(i.name))"
                        item-value="value"
                        clearable
                        single-line hide-details
                        @change="updateFilter"
              />
            </v-flex>

            <v-flex xs12 sm6>
              <v-combobox v-model="filters.country_code"
                          :label="$t('forms.fields.structureCountry')"
                          :items="countries"
                          :item-text="countryTl"
                          clearable
                          single-line hide-details
                          @change="updateFilter"
              />
            </v-flex>

            <v-flex xs12 sm12 md6>
              <v-select v-model="filters.networks"
                        :label="$t('forms.fields.network')"
                        :items="$store.getters['network/all']"
                        :item-text="(i => $t(i.name))"
                        item-value="id"
                        clearable
                        multiple
                        single-line hide-details
                        @change="updateFilter"
              />
            </v-flex>

            <v-flex xs12 sm6>
              <v-select v-model="filters.knowledge_areas"
                        :label="$t('forms.fields.knowledgeArea')"
                        :items="$store.getters['knowledgearea/all']"
                        :item-text="(i => $t(i.name))"
                        item-value="id"
                        clearable
                        single-line hide-details
                        @change="updateFilter"
              />
            </v-flex>
            <!-- End of Filters -->
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 class="hidden-sm-and-down">
      <v-layout row wrap>
        <v-flex v-for="structure in structures" :key="structure.id" xs12 sm6 md4 lg3 xl2 mb-3>
          <StructureCard :structure="structure" />
        </v-flex>
      </v-layout>
    </v-flex>

    <v-flex xs12 class="hidden-md-and-up">
      <v-card>
        <ModelList :objects="structures" show-last-modified="true" />
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
            @click="loadMoreStructures"
          >
            {{ $t('pages.structureList.showMore') }}
          </v-btn>

          <v-btn v-else disabled>
            {{ $t('pages.structureList.noMoreStructures') }}
          </v-btn>
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>


<script>
import StructureCard from "@/components/structure/StructureCard";
import ModelList from "@/components/generic/ModelList";

import { debounce, cloneDeep } from "lodash";
import { Countries } from "@/plugins/i18n";

export default {

  metaInfo() {
    return {
      title: this.$t('noums.structures')
    };
  },

  components: {
    StructureCard,
    ModelList
  },

  data() {
    return {
      countries: Countries,
      filters : {},
      
      page: 0,
      pagesize: 12,

      canLoadMore: false,
      loadMoreDisabled: false,
    }
  },

  computed: {
    structures() {
      let list = this.$store.getters["structure/all"].slice();
      list.sort((a,b) => b.modified_at.localeCompare(a.modified_at))
      return list
    }
  },

  async mounted(){
    // Data we need
    this.$store.dispatch("knowledgearea/load")
    this.$store.dispatch("network/load")

    // debouncer
    this.updateFilter = debounce(this.updateFilter, 250);

    // Get URL parameters
    let queryParams = this.$route.query;
    if(queryParams.country_code){
      this.filters.country_code = this.countries.filter(c => c.alpha3Code == queryParams.country_code)[0]
    }
  
    // Load page 0
    this.$store.dispatch("structure/clear")
    await this.loadStructurePage();
  },

  methods: {
    async loadStructurePage(){
      let filters = cloneDeep(this.filters);

      let params = {
        offset: this.page * this.pagesize,
        limit: this.pagesize
      }

      // TODO: multivalued filters?
      // if(filters.networks)
      //   filters.networks = filters.networks.join(',')

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
      let countBefore = this.$store.getters['structure/all'].length

      await this.$store.dispatch("structure/load", { params })

      let countAfter = this.$store.getters['structure/all'].length
      this.canLoadMore = countAfter - countBefore == this.pagesize

      // special check on page 1
      if(this.page == 0)
        this.canLoadMore = countAfter == this.pagesize;
    },

    async loadMoreStructures(){
      this.loadMoreDisabled = true;
      // Load next batch
      this.page += 1;
      await this.loadStructurePage();
      // Increase page
      this.loadMoreDisabled = false;
    },

    async updateFilter(){
      this.$store.dispatch('structure/clear');
      this.page = 0;
      this.loadStructurePage();
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

