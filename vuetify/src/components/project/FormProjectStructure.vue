<template>
  <v-form v-if="project" ref="form" v-model="valid">
    <h2>Associated Intermediation Structure</h2>
    <p />

    <p class="subheading">
      Select under which Intermediation Structure your project is established.
    </p>

    <v-alert color="info"
             :value="isReadOnly && !project.collaboration.is_approved"
             class="subheading"
    >
      <v-icon dark>
        info
      </v-icon>
      The structure has yet to approve your Project before it will be shown in
      the website.
    </v-alert>
    <p v-if="isReadOnly && !project.collaboration.is_approved" />

    <v-combobox
      ref="structureCB"
      v-model="project.collaboration.structure"
      box
      :items="structureSearch"
      :rules="[rules.isStructure, rules.required]"
      :readonly="isReadOnly"
      label="Intermediation Structure"
      cache-items
      item-text="name"
      item-value="id"
      chips
      deletable-chips
      @update:searchInput="updateStructureSearch($event)"
      @input="clearSearch('structureCB')"
    />

    <v-btn v-if="!isReadOnly" block large
           color="success"
           :disabled="!valid || processing"
           :loading="processing"
           @click="attemptSubmit()"
    >
      {{ $t('actions.save') }}
    </v-btn>

    <v-btn v-if="isReadOnly" block large
           color="error"
           :disabled="!valid || processing"
           :loading="processing"
           @click="deleteCollaboration()"
    >
      {{ $t('actions.delete') }}
    </v-btn>
  </v-form>
</template>


<script>
export default {
  props: ["processing", "projectId"],

  data() {
    return {
      valid: null,
      rules: {
        isStructure: v => this.isStructure(v) || this.$t("forms.rules.mustBeStructure"),
        required: v => !!v || this.$t("forms.rules.mustBeStructure"),
      },
      structureSearch: [],
      project: null,
      isReadOnly: false
    };
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"]
    }
  },

  async mounted() {
    let store = this.$store

    // Load structures and project
    await store.dispatch("structure/load");
    await store.dispatch("project/load", [this.projectId]);

    this.structureSearch = this.structures.slice(0,5)
    this.project = store.getters["project/detail"](this.projectId)

    if(this.project.collaboration == null){
      // Create new collab if project is currently free
      this.project.collaboration = {
        project: this.projectId,
        structure: null
      }
    }else{
      // Existing Collaboration
      let structureId = this.project.collaboration.structure
      this.project.collaboration.structure = store.getters['structure/get'](structureId)
      this.isReadOnly = true
    }

  },

  methods: {
    attemptSubmit() {
      if (this.$refs.form.validate()) {
        let collab = {...this.project.collaboration}
        collab.structure = collab.structure.id
        this.$emit("submit", collab);
      }
    },

    deleteCollaboration(){
      alert("not implemented")
    },

    isStructure(value){
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