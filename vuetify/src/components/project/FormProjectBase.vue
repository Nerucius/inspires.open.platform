<template>
  <v-form ref="form" v-model="valid">
    <h2 class="mb-2">
      Project Details
    </h2>

    <p class="subheading">
      Define your project information.
    </p>

    <v-text-field
      v-model="editedProject.acronym"
      box
      :rules="[rules.required]"
      counter="10"
      maxlength="10"
      label="Project Acronym"
      hint="Choose a Project Acronim."
    />

    <v-text-field
      v-model="editedProject.name"
      box
      :rules="[rules.required]"
      counter="50"
      label="Project Name"
      hint="Choose a name that characterizes your project.
                Less than 50 characters suggested."
    />

    <v-textarea
      v-model="editedProject.summary"
      box
      counter="200"
      label="Project Summary"
      hint="A short summary of your project and what it encompasses.
                Suggested to keep it under 200 characters."
    />

    <h2 class="mb-2">
      Project Administrators
    </h2>
    <p class="subheading">
      Project administrators have full access to the project and can edit the project's
      details as well as add and remove other administrators and participants. These permissions
      apply only within the platform.
    </p>

    <v-combobox ref="managersCB"
                v-model="editedProject.managers"
                box
                :items="userSearch"
                :rules="[rules.isUser]"
                label="Project Managers"
                item-text="full_name"
                item-value="id"
                multiple
                chips
                deletable-chips
                @update:searchInput="updateUserSearch($event)"
                @input="clearSearch('managersCB')"
    />

    <!-- Expanded details, only after save -->
    <template v-if="editedProject.id">
      <h2 class="mb-2">
        Additional Information
      </h2>

      <p class="subheading">
        Other useful details so that your project is well defined and can be found in searches.
      </p>

      <v-text-field
        v-model="editedProject.contact_email"
        box
        label="Contact Email"
        hint="Where should people reach you with questions about the project?"
      />
      <v-text-field
        v-model="editedProject.contact_website"
        box
        label="Project Homepage"
        hint="Homepage or website of the project"
      />

      <v-select
        v-model="editedProject.project_type"
        box
        :items="projectTypes"
        label="Project Type"
      />

      <v-select
        v-model="editedProject.knowledge_area"
        box
        :items="knowledgeAreas"
        label="Knowledge Area"
        :item-text="kaName"
        item-value="id"
      />

      <v-textarea
        v-model="editedProject.description"
        box
        label="Project Description"
        hint="Long-form project description."
        rows="8"
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
  props: ["project"],

  data() {
    return {
      processing: false,
      valid: null,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
      userSearch: [],
      editedProject: {},
      roles: [
        {id:1, name:"Scientist"},
        {id:2, name:"Student"},
        {id:3, name:"Civil Society"},
      ],
      projectTypes: [
        {value:"research", text:"Research"},
        {value:"publicEngagement", text:"Public Engagement"},
        {value:"serviceLearning", text:"Service Learning"},
      ],
    };
  },

  computed:{
    knowledgeAreas(){
      return this.$store.getters["knowledgearea/all"]
    }
  },

  mounted: async function() {

    if (this.project && this.project.id) {
      // Editing existing project
      this.editedProject = this.loadProject()
      this.$store.dispatch("knowledgearea/load")

    }else{
      // New Project
      this.editedProject.managers = [
        this.$store.getters["user/current"]
      ];
    }

    // Initialize user search with all visible users
    // this.userSearch = [...this.editedProject.participants, ...this.editedProject.managers]
  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
    },

    kaName(knowledgeArea){
      return `[${knowledgeArea.code}] ${this.$t(knowledgeArea.name)}`
    },

    loadProject: function(){
      let loadedProject = cloneDeep(this.project)

      // Transform attributes to be compatible with Form
      loadedProject.managers = (loadedProject.managers || []).map(id => this.user(id))
      loadedProject.participants = (loadedProject.participants || []).map(part =>
        ({...this.user(part.user), role: part.role, partId: part.id})
      )

      return loadedProject
    },

    attemptSubmit: async function() {
      if (!this.$refs.form.validate()) {
        console.error("Form failed to validate")
        return
      }

      this.processing = true
      let project = cloneDeep(this.editedProject);
      project.managers = project.managers.map(u => u.id)

      // In the case of no id, send event to parent to create project
      if(!project.id){
        this.$emit("create", project)
        return
      }

      try{
        await this.$store.dispatch("project/update", project)
        this.$store.dispatch("toast/success", this.$t('forms.toasts.projectSaveSuccess'))

        if(this.project.id){
          // Reload project to get updated IDS
          this.editedProject = this.loadProject()
        }

      } catch(err){
        // Failed to save
        this.$store.dispatch("toast/error", this.$t('forms.toasts.projectSaveFailure'))
      }

      this.processing = false


    },

    isUser(value){
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