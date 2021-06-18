<template>
  <v-form v-if="project" ref="form" v-model="valid">
    <!-- Title -->
    <v-layout>
      <v-flex grow>
        <h2>{{ $t('pages.projectManage.structurePartnersTitle') }}</h2>
      </v-flex>
      <v-flex shrink>
        <v-btn class="elevation-0" fab :outline="!showHelp" :dark="showHelp" small color="blue" @click="showHelp = !showHelp">
          <v-icon>mdi-help</v-icon>
        </v-btn>
      </v-flex>
    </v-layout>

    <p class="subheading">
      {{ $t('pages.projectManage.structurePartnersSubheading') }}
    </p>

    <ModelList :show-last-modified="false" :objects="partners" />

    <div class="mt-4" />

    <v-combobox
      ref="structureCB"
      v-model="partners"
      box multiple
      :items="structureSearch"
      :rules="[rules.isStructure]"
      label="Partner Structures"
      item-text="name"
      item-value="id"
      chips deletable-chips
      @update:searchInput="updateStructureSearch($event)"
      @input="clearSearch('structureCB')"
    />

    <v-btn block large
           color="success"
           :disabled="!valid || processing"
           :loading="processing"
           @click="attemptSubmit()"
    >
      {{ $t('actions.save') }}
    </v-btn>

  </v-form>
</template>


<script>
import ModelList from "@/components/generic/ModelList";

export default {
  components:{
    ModelList
  },

  props: ["project"],

  data() {
    return {
      showHelp: false,
      valid: null,
      rules: {
        isStructure: v => this.isStructure(v) || this.$t("forms.rules.mustBeStructure")
      },
      partners: [],
      structureSearch: [],
      processing: false,
    };
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"]
    }
  },

  async created() {
    let store = this.$store

    // Load structures and project
    await Promise.all([
      store.dispatch("structure/load"),
    ])

    // Convert to partners
    this.partners = this.project.collaboration.partners.map(sid => store.getters["structure/get"](sid))
    this.structureSearch = store.getters["structure/all"].slice(0,5)
  },

  methods: {
    attemptSubmit: async function() {
      if (this.$refs.form.validate()) {

        let collab = {
          id: this.project.collaboration.id,
          partners: this.partners.map(p => p.id)
        }

        this.processing = true

        try{
          await this.$store.dispatch("collaboration/update", collab)
          this.$store.dispatch("toast/success", this.$t('forms.toasts.saveSuccess'))

        } catch(error){
          this.$store.dispatch("toast/error", {
            message: this.$t('forms.toasts.saveFailure'),
            error
          })
        }
        this.processing = false
      }
    },


    isStructure(value){
      return true
      if (!value) return true
      // Check that all object are user instances
      return !(value.id == undefined)
    },

    clearSearch(ref) {
      this.$refs[ref].lazySearch = "";
    },

    updateStructureSearch(term) {
      term = term || "";
      if (term.length < 2) {
        this.structureSearch = [];
        return;
      }
      term = new RegExp(term, "gi");
      this.structureSearch = this.structures
        .filter(u => u.name.match(term))
        .slice(0, 5);
    }
  }
};
</script>
