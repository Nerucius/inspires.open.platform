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
              Want to know more about structures?
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
      <v-card class="elevation-1">
        <v-card-text>
          <h3>{{ $t('actions.search') }}</h3>
          <v-layout wrap>
            <v-flex xs12 sm6 md4>
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

            <v-flex xs12 sm6 md4>
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

            <v-flex xs12 sm6 md4>
              <v-combobox v-model="filters.country_code"
                          :label="$t('forms.fields.structureCountry')"
                          :items="countries"
                          :item-text="countryTl"
                          clearable
                          single-line hide-details
                          @change="updateFilter"
              />
            </v-flex>
            
            <!-- <v-flex xs12>
              <v-combobox v-model="filters.collaboration__structure"
                :label="$t('forms.fields.structureName')"
                :items="$store.getters['structure/all']"
                item-text="name"
                clearable
                single-line hide-details
                @change="updateFilter"
              />
            </v-flex> -->
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-layout row wrap>
        <v-flex v-for="structure in structures" :key="structure.id" xs12 sm6 md4 lg3 xl2 mb-3>
          <StructureCard :structure="structure" />
        </v-flex>
      </v-layout>
    </v-flex>
  </v-layout>
</template>


<script>
import StructureCard from "@/components/structure/StructureCard";
import { debounce } from "lodash";
import { Countries } from "@/plugins/i18n";

export default {

  metaInfo() {
    return {
      title: this.$t('noums.structures')
    };
  },

  components: {
    StructureCard
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
    this.$store.dispatch("structure/load")

    // debouncer
    this.updateFilter = debounce(this.updateFilter, 250);
  
    // Load page 0
    this.$store.dispatch("structure/clear")
    await this.loadStructurePage();
  },

  methods: {
    async loadStructurePage(){
      let filters = this.filters;

      let params = {
        ordering: "-modified_at",
        offset: this.page * this.pagesize,
        limit: this.pagesize
      }

      // TODO: multivalued filters?

      params = {
        ...params,
        ...filters,
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

