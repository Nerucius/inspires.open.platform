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
      :hint="$t('forms.hints.projectAcronym')"
      :label="$t('forms.fields.projectAcronym')"
    />

    <v-text-field
      v-model="editedProject.name"
      box
      :rules="[rules.required]"
      counter="50"
      :hint="$t('forms.hints.projectName')"
      :label="$t('forms.fields.projectName')"
    />

    <v-textarea
      v-model="editedProject.summary"
      box
      counter="200"
      :hint="$t('forms.hints.projectSummary')"
      :label="$t('forms.fields.projectSummary')"
    />

    <v-textarea v-if="editedProject.id"
                v-model="editedProject.description"
                :label="$t('forms.fields.description')"
                :hint="$t('forms.hints.description')"
                box
                rows="8"
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
                no-filter
                :items="userSearch"
                :rules="[rules.isUser]"
                :hint="$t('forms.hints.projectAdministrators')"
                :label="$t('forms.fields.projectAdministrators')"
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

      <v-select
        v-model="editedProject.knowledge_area"
        box
        :items="knowledgeAreas"
        :label="$t('forms.fields.knowledgeArea')"
        :hint="$t('forms.hints.knowledgeArea')"
        :item-text="kaName"
        item-value="id"
      />

      <v-select v-model="editedProject.country_code"
                box
                :items="Countries"
                :item-text="localizedCountryName"
                item-value="alpha3Code"
                :label="$t('forms.fields.projectCountry')"
                :hint="$t('forms.hints.projectCountry')"
      />

      <v-select
        v-model="editedProject.project_type"
        box
        :items="projectTypes"
        :label="$t('forms.fields.projectType')"
        :hint="$t('forms.hints.projectType')"
      />


      <v-text-field
        v-model="editedProject.image_url"
        box
        :rules="[rules.isURL]"
        :hint="$t('forms.hints.projectImageURL')"
        :label="$t('forms.fields.projectImageURL')"
      />

      <h3 class="mb-2">
        Contact Information
      </h3>

      <v-textarea
        v-model="editedProject.contact_postal_address"
        box
        :label="$t('forms.fields.postalAddress')"
        :hint="$t('forms.hints.postalAddress')"
      />

      <v-text-field
        v-model="editedProject.contact_email"
        box
        :rules="[rules.isEmail]"
        :label="$t('forms.fields.contactEmail')"
        :hint="$t('forms.hints.contactEmail')"
      />
      <v-text-field
        v-model="editedProject.contact_website"
        box
        :rules="[rules.isURL]"
        :label="$t('forms.fields.contactWebsite')"
        :hint="$t('forms.hints.contactWebsite')"
      />

      <v-text-field
        v-model="editedProject.contact_social_facebook"
        box
        :rules="[rules.isURL]"
        label="Facebook"
        hint="Facebook page if applicable"
      />
      <v-text-field
        v-model="editedProject.contact_social_twitter"
        box
        :rules="[rules.isURL]"
        label="Twitter"
        hint="Twitter page if applicable"
      />
      <v-text-field
        v-model="editedProject.contact_social_other"
        box
        :rules="[rules.isURL]"
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
import { Countries } from '@/plugins/i18n'
import { regexIsURL, regexIsEmail } from '@/plugins/utils'

export default {
  props: ["project"],

  data() {
    return {
      Countries,
      processing: false,
      valid: null,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        isURL: v => regexIsURL(v) || this.$t("forms.rules.mustBeURL"),
        isEmail: v => regexIsEmail(v) || this.$t("forms.rules.mustBeEmail"),
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
        {value:"RESEARCH", text:"Research"},
        {value:"PARTICIPATORY_RESEARCH", text:"Participatory Research"},
        {value:"PARTICIPATORY_ACTION_RESEARCH", text:"Participatory Action Research"},
        {value:"CITIZEN_SCIENCE", text:"Citizen Science"},
        {value:"PUBLIC_ENGAGEMENT", text:"Public Engagement"},
        {value:"SERVICE_LEARNING", text:"Service Learning"},
        {value:"ADVOCACY", text:"Advocacy"},
        {value:"INNOVATION", text:"Innovation"},
        {value:"POLICY_INNOVATION", text:"Policy Innovation"},
        {value:"OTHER", text:"Other"},
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

    localizedCountryName(country){
      let locale = this.$i18n.locale
      return country.translations[locale] || country.name
    },

    attemptSubmit: async function() {
      if (!this.$refs.form.validate()) {
        return
      }

      this.processing = true
      let project = cloneDeep(this.editedProject);
      project.managers = project.managers.map(u => u.id)

      // In the case of no id, send event to parent to create project
      if(!project.id){
        this.$emit("create", project)
        // re-enable button after 2 seconds
        setTimeout(()=>{ this.processing = false }, 2000)
        return
      }

      try{
        await this.$store.dispatch("project/update", project)
        this.$store.dispatch("toast/success", this.$t('forms.toasts.projectSaveSuccess'))

        if(this.project.id){
          // Reload project to get updated IDS
          this.editedProject = this.loadProject()
        }

      } catch(error){
        // Failed to save
        this.$store.dispatch("toast/error", {
          message:this.$t('forms.toasts.projectSaveFailure'), error
        })
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