<template>
  <v-form ref="form" v-model="valid">
    <h2 class="mb-2">
      {{ $t('pages.projectManage.infoTitle') }}
    </h2>

    <p class="subheading">
      {{ $t('pages.projectManage.infoDescription') }}
    </p>

    <v-text-field
      v-model="editedProject.acronym"
      box
      :rules="[rules.required]"
      counter="10"
      maxlength="10"
      :label="$t('forms.fields.projectAcronym')"
      :hint="$t('forms.hints.projectAcronym')"
    />

    <v-text-field
      v-model="editedProject.name"
      box
      :rules="[rules.required]"
      counter="50"
      :label="$t('forms.fields.projectName')"
      :hint="$t('forms.hints.projectName')"
    />

    <v-textarea
      v-model="editedProject.summary"
      box
      :rules="[rules.required]"
      counter="200"
      :label="$t('forms.fields.summary')"
      :hint="$t('forms.hints.projectSummary')"
    />

    <h3 class="mb-2">
      {{ $t('forms.fields.projectAdministrators') }}
    </h3>
    <p class="subheading">
      {{ $t('forms.descriptions.projectAdministrators') }}
    </p>

    <v-combobox
      ref="managersCB"
      v-model="editedProject.managers"
      box
      no-filter
      :items="userSearch"
      :rules="[rules.isUser]"
      :label="$t('forms.fields.projectAdministrators')"
      :hint="$t('forms.hints.projectAdministrators')"
      item-text="form_name"
      item-value="id"
      multiple
      chips
      deletable-chips
      @update:searchInput="updateUserSearch($event)"
      @input="clearSearch('managersCB')"
    />

    <p class="mb-3" />

    <!-- Expanded details, only after save -->
    <template v-if="editedProject.id">
      <h2 class="mb-2">
        {{ $t('pages.projectManage.infoAdditionalTitle') }}
      </h2>

      <p class="subheading">
        {{ $t('pages.projectManage.infoAdditionalDescription') }}
      </p>

      <h3 class="mb-2">
        {{ $t('forms.fields.description') }}
      </h3>

      <p class="subheading">
        {{ $t('forms.hints.description') }}
        {{ $t('forms.hints.descriptionTemplate') }}
      </p>

      <v-textarea
        v-model="editedProject.description"
        box
        rows="26"
        :label="$t('forms.fields.description')"
        :hint="$t('forms.hints.description')"
      />

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
        :items="$store.getters['project/projectTypes']"
        :item-text="e => $t(e.name)"
        :label="$t('forms.fields.projectType')"
        :hint="$t('forms.hints.projectType')"
      />

      <h3 class="mb-2">
        {{ $t('forms.fields.coverImage') }}
      </h3>

      <ImageUpload
        v-model="editedProject.image_url"
        :title="`project-cover-${project.id}`"
        @change="saveImage($event)"
      />

      <h3 class="mb-2">
        {{ $t('pages.projectManage.infoContactTitle') }}
      </h3>

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
      <v-textarea
        v-model="editedProject.contact_postal_address"
        box
        :label="$t('forms.fields.postalAddress')"
        :hint="$t('forms.hints.postalAddress')"
      />
      <v-text-field
        v-model="editedProject.contact_social_facebook"
        box
        :rules="[rules.isURL, rules.isFacebook]"
        label="Facebook"
      />
      <v-text-field
        v-model="editedProject.contact_social_twitter"
        box
        :rules="[rules.isURL, rules.isTwitter]"
        label="Twitter"
      />
      <v-text-field
        v-model="editedProject.contact_social_other"
        box
        :rules="[rules.isURL]"
        label="Social Networks"
      />
    </template>


    <!-- Save button -->
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
import ImageUpload from "@/components/input/ImageUpload";

export default {
  components: {ImageUpload},

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
        isTwitter: v => !v || v.indexOf('twitter.com') >= 0 || this.$t("forms.rules.mustBeURL"),
        isFacebook: v => !v || v.indexOf('facebook.com') >= 0 || this.$t("forms.rules.mustBeURL"),
        isEmail: v => regexIsEmail(v) || this.$t("forms.rules.mustBeEmail"),
      },
      userSearch: [],
      editedProject: {},
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

    setTimeout(() => {
      this.$refs.form.validate()
    }, 500);

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

    saveImage: async function(image_url) {
      try{
        await this.$store.dispatch("project/update", {id:this.project.id, image_url})
        this.$store.dispatch("toast/success", this.$t('forms.toasts.saveImageSuccess'))
      }catch (error){
        this.$store.dispatch("toast/error", {message: this.$t('forms.toasts.saveImageFailure'), error})
      }
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
          message:this.$t('forms.toasts.projectSaveFailure'),
          error
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