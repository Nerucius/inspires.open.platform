<template>
  <v-form ref="form" v-model="valid">
    <h2 class="mb-2">
      Structure Details
    </h2>

    <p class="subheading">
      Basic details about the structure.
    </p>

    <v-text-field
      v-model="editedStructure.name"
      box
      :rules="[rules.required]"
      counter="50"
      label="Structure Name"
      hint="Choose a name that characterizes your structure.
                Less than 50 characters suggested."
    />

    <v-textarea
      v-model="editedStructure.summary"
      box
      counter="200"
      label="Structure Summary"
      hint="A short summary of your structure and what it encompasses.
                Suggested to keep it under 200 characters."
    />

    <h2 class="mb-2">
      Structure Managers
    </h2>
    <p class="subheading">
      Structure managers have full access to the structure and can edit the structure's
      details as well as add and remove managers and participants.
    </p>

    <v-combobox ref="managersCB"
                v-model="editedStructure.managers"
                box
                :items="userSearch"
                :rules="[rules.isUser]"
                label="Structure Managers"
                item-text="full_name"
                item-value="id"
                multiple
                chips
                deletable-chips
                @update:searchInput="updateUserSearch($event)"
                @input="clearSearch('managersCB')"
    />

    <!-- Expanded details, only after save -->
    <template v-if="editedStructure.id">
      <h2 class="mb-2">
        Additional Information
      </h2>

      <h3 class="mb-2">
        Knowledge Areas
      </h3>

      <v-combobox v-model="editedStructure.knowledge_areas"
                  box
                  label="List of Knowledge Areas"
                  hint="Select all knowledge areas of research under this structure."
                  multiple
                  chips
                  deletable-chips
                  :rules="[rules.isKnowledgeArea]"
                  :items="knowledgeAreas"
                  item-text="code_name"
                  item-value="id"
      />

      <h3 class="mb-2">
        Detailed description
      </h3>

      <v-textarea
        v-model="editedStructure.description"
        box
        label="Description"
        hint="Long-form structure description."
        rows="8"
      />

      <h3 class="mb-2">
        Poster Image
      </h3>
      <v-text-field
        v-model="editedStructure.image_url"
        box
        label="URL to an image"
        hint="Shown in listings as well as the structures's page"
      />

      <h3 class="mb-2">
        Contact Information
      </h3>

      <v-text-field
        v-model="editedStructure.contact_email"
        box
        label="Contact Email"
        hint="Where should people reach you with questions about the structure?"
      />
      <v-text-field
        v-model="editedStructure.contact_website"
        box
        label="Homepage / Website"
        hint="Homepage or website of the structure"
      />
      <v-textarea
        v-model="editedStructure.contact_postal_address"
        box
        label="Postal Address"
        hint="Physical Mailing address for postal mail"
      />
      <v-text-field
        v-model="editedStructure.contact_social_facebook"
        box
        label="Facebook"
        hint="Facebook page if applicable"
      />
      <v-text-field
        v-model="editedStructure.contact_social_twitter"
        box
        label="Twitter"
        hint="Twitter page if applicable"
      />
      <v-text-field
        v-model="editedStructure.contact_social_other"
        box
        label="Other social networks"
        hint=""
      />
    </template>


    <v-btn block large color="success"
           :disabled="!valid || processing"
           :loading="processing"
           @click="attemptSubmit()"
    >
      {{ $t('actions.save') }}
    </v-btn>
  </v-form>
</template>


<script>
import { cloneDeep } from "lodash";

export default {
  props: ["structure"],

  data() {
    return {
      processing: false,
      valid: null,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        isKnowledgeArea: v => this.isKnowledgeArea(v) || this.$t("forms.rules.mustBeKnowledgeArea"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
      userSearch: [],
      editedStructure: {},

    };
  },

  computed:{
    knowledgeAreas(){
      return this.$store.getters["knowledgearea/all"]
    }
  },

  mounted: async function() {

    if (this.structure && this.structure.id) {
      // Editing existing structure
      this.editedStructure = this.loadStructure()

    }else{
      // New structure
      this.editedStructure.managers = [
        this.$store.getters["user/current"]
      ];
    }

    // Initialize user search with all visible users
    // this.userSearch = [...this.editedStructure.participants, ...this.editedStructure.managers]
  },

  methods: {
    user(id){
      return this.$store.getters['user/get'](id)
    },

    knowledgeArea(id){
      return this.$store.getters['knowledgearea/get'](id)
    },

    loadStructure: function(){
      let loadedStructure = cloneDeep(this.structure)
      // Transform attributes to be compatible with Form
      loadedStructure.managers = (loadedStructure.managers || []).map(id => this.user(id))
      loadedStructure.knowledge_areas = (loadedStructure.knowledge_areas || []).map(id => this.knowledgeArea(id))

      return loadedStructure
    },

    attemptSubmit: async function() {
      if (!this.$refs.form.validate()) {
        console.error("Form failed to validate")
        return
      }

      this.processing = true
      let structure = cloneDeep(this.editedStructure);
      structure.managers = structure.managers.map(u => u.id)

      // In the case of no id, send event to parent to create structure
      if(!structure.id){
        this.$emit("create", structure)
        return
      }

      // Map knowledge areas
      structure.knowledge_areas = structure.knowledge_areas.map(u => u.id)

      let message
      try{
        await this.$store.dispatch("structure/update", structure)
        message = this.$t('pages.structureManage.success')
      } catch(err){
        message = this.$t('pages.structureManage.failure')
      }
      this.processing = false

      // Reload structure to get updated IDS
      await this.$store.dispatch("structure/load", [structure.id])
      this.editedStructure = this.loadStructure()

    },

    isUser(value){
      // Check that all object are user instances
      if (!value) return true
      return !value.map(item => item.id == undefined).some(v => !!v)
    },

    isKnowledgeArea(value){
      // Check that all object are user instances
      if (!value) return true
      return !value.map(item => item.id == undefined).some(v => !!v)
    },

    clearSearch(ref) {
      this.$refs[ref].lazySearch = "";
    },

    updateUserSearch(term) {
      term = term || "";
      if (term.length < 2) {
        this.userSearch = [];
        return;
      }
      term = new RegExp(term, "gi");
      this.userSearch = cloneDeep(
        this.$store.getters["user/all"]
        .filter(u => u.username.match(term) || u.full_name.match(term))
        .slice(0, 5)
      )
    }
  }
};
</script>