<template>
  <v-form v-if="project" ref="form" v-model="valid">
    <h2>Associated Intermediation Structure</h2>
    <p />

    <p class="subheading">
      Select under which Intermediation Structure your project is established.
    </p>

    <v-alert color="info"
             :value="isReadOnly && !collaboration.is_approved"
             class="subheading"
    >
      <v-icon dark>
        info
      </v-icon>
      The structure has yet to approve your Project before it will be shown in
      the website.
    </v-alert>
    <p v-if="isReadOnly && !collaboration.is_approved" />

    <v-combobox
      ref="structureCB"
      v-model="collaboration.structure"
      box
      :items="structureSearch"
      :rules="[rules.isStructure, rules.required]"
      :readonly="isReadOnly"
      label="Intermediation Structure"
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
  props: ["project"],

  data() {
    return {
      valid: null,
      rules: {
        isStructure: v => this.isStructure(v) || this.$t("forms.rules.mustBeStructure"),
        required: v => !!v || this.$t("forms.rules.mustBeStructure"),
      },
      collaboration: {},
      structureSearch: [],
      processing: false,
    };
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"]
    },
    isReadOnly(){
      return !!this.collaboration.id
    }
  },

  async mounted() {
    let store = this.$store

    // Load structures and project
    await store.dispatch("structure/load");
    this.structureSearch = this.structures.slice(0,5)

    if(this.project.collaboration != null){
      // Existing Collaboration
      let structureId = this.project.collaboration.structure
      let structure = store.getters["structure/get"](structureId)
      this.collaboration = {
        id: this.project.collaboration.id,
        project: this.projectId,
        structure: structure
      }
    }

  },

  methods: {
    attemptSubmit: async function() {
      if (this.$refs.form.validate()) {

        let collab = {
          project: this.project.id,
          structure: this.collaboration.structure.id
        }

        this.processing = true
        let message

        try{
          let result = (await this.$store.dispatch("collaboration/create", collab)).body
          // overwrite data
          this.collaboration = result
          this.collaboration.structure = this.$store.getters["structure/get"](result.structure)
          console.log(result)

          message = this.$t('pages.projectManage.collaborationSuccess')
        } catch(err){
          message = this.$t('pages.projectManage.collaborationSuccess')
        }

        this.processing = false
        // this.$store.dispatch("snackbar/show", {message})
      }
    },

    deleteCollaboration(){
      let alertMessage = this.$t('pages.projectManage.deleteCollaborationAlert')
      if(confirm(alertMessage)){
        this.$store.dispatch("collaboration/delete", this.collaboration.id)

        // Reset collaboration
        this.structureSearch = this.structures.slice(0,5)
        this.collaboration = {}
      }

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