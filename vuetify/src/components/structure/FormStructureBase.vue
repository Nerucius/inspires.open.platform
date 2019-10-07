<template>
  <v-form ref="form" v-model="valid">
    <h2 class="mb-2">
      {{ $t('pages.structureManage.infoTitle') }}
    </h2>

    <p class="subheading">
      {{ $t('pages.structureManage.infoDescription') }}
    </p>

    <v-text-field
      v-model="editedStructure.name"
      box
      :rules="[rules.required]"
      counter="50"
      :label="$t('forms.fields.structureName')"
      :hint="$t('forms.hints.structureName')"
    />

    <v-textarea
      v-model="editedStructure.summary"
      box
      :rules="[rules.required]"
      counter="200"
      :label="$t('forms.fields.summary')"
      :hint="$t('forms.hints.structureSummary')"
    />

    <v-textarea
      v-if="editedStructure.id"
      v-model="editedStructure.description"
      box
      rows="8"
      :label="$t('forms.fields.description')"
      :hint="$t('forms.hints.description')"
    />

    <h2 class="mb-2">
      {{ $t('pages.structureManage.infoAdministratorsTitle') }}
    </h2>
    <p class="subheading">
      {{ $t('pages.structureManage.infoAdministratorsDescription') }}
    </p>

    <v-combobox
      ref="managersCB"
      v-model="editedStructure.managers"
      box
      no-filter
      :items="userSearch"
      :rules="[rules.isUser]"
      :label="$t('forms.fields.structureAdministrators')"
      :hint="$t('forms.hints.structureAdministrators')"
      item-text="form_name"
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
        {{ $t('pages.projectManage.infoAdditionalTitle') }}
      </h2>

      <v-select
        v-model="editedStructure.structure_type"
        box
        :items="$store.getters['structure/structureTypes']"
        :item-text="e => $t(e.name)"
        :label="$t('forms.fields.structureType')"
        :hint="$t('forms.hints.structureType')"
      />


      <v-select
        v-model="editedStructure.country_code"
        box
        :items="Countries"
        :item-text="localizedCountryName"
        item-value="alpha3Code"
        :label="$t('forms.fields.structureCountry')"
        :hint="$t('forms.hints.structureCountry')"
      />

      <v-text-field
        v-model="editedStructure.year_founded"
        box
        min="500"
        max="2100"
        type="number"
        :label="$t('forms.fields.structureYearFounded')"
      />


      <h3 class="mb-2">
        {{ $t('forms.fields.knowledgeAreas') }}
      </h3>

      <v-combobox
        v-model="editedStructure.knowledge_areas"
        box
        :label="$t('forms.fields.knowledgeAreas')"
        :hint="$t('forms.hints.knowledgeAreas')"
        multiple
        chips
        deletable-chips
        :rules="[rules.isKnowledgeArea]"
        :items="knowledgeAreas"
        :item-text="kaName"
        item-value="id"
      />

      <h3 class="mb-2">
        {{ $t('forms.fields.coverImage') }}
      </h3>
      <ImageUpload
        v-model="editedStructure.image_url"
        :title="`structure-cover-${structure.id}`"
        @change="saveImage($event)"
      />

      <!-- <v-text-field
        v-model="editedStructure.image_url"
        box
        :rules="[rules.isURL]"
        label="URL to an image"
        hint="Shown in listings as well as the structures's page"
      /> -->

      <h3 class="mb-2">
        {{ $t('pages.projectManage.infoContactTitle') }}
      </h3>

      <v-text-field
        v-model="editedStructure.contact_email"
        box
        :rules="[rules.isEmail]"
        :label="$t('forms.fields.contactEmail')"
        :hint="$t('forms.hints.contactEmail')"
      />
      <v-text-field
        v-model="editedStructure.contact_website"
        box
        :rules="[rules.isURL]"
        :label="$t('forms.fields.contactWebsite')"
        :hint="$t('forms.hints.contactWebsite')"
      />
      <v-textarea
        v-model="editedStructure.contact_postal_address"
        box
        :label="$t('forms.fields.postalAddress')"
        :hint="$t('forms.hints.postalAddress')"
      />
      <v-text-field
        v-model="editedStructure.contact_social_facebook"
        box
        :rules="[rules.isURL, rules.isFacebook]"
        label="Facebook"
      />
      <v-text-field
        v-model="editedStructure.contact_social_twitter"
        box
        :rules="[rules.isURL, rules.isTwitter]"
        label="Twitter"
      />
      <v-text-field
        v-model="editedStructure.contact_social_other"
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
import { regexIsURL,regexIsEmail } from '@/plugins/utils'
import ImageUpload from "@/components/input/ImageUpload";

export default {
  components: { ImageUpload },

  props: ["structure"],

  data() {
    return {
      Countries,
      processing: false,
      valid: null,
      rules: {
        // required: v => true,
        // isUser: v => true,
        // isURL: v => true,
        isEmail: v => true,
        isCountry: v => true,
        isKnowledgeArea: v => true,
        minlen: v => true,

        required: v => !!v || this.$t("forms.rules.requiredField"),
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        isURL: v => regexIsURL(v) || this.$t("forms.rules.mustBeURL"),
        isTwitter: v => !v || v.indexOf('twitter.com') >= 0 || this.$t("forms.rules.mustBeURL"),
        isFacebook: v => !v || v.indexOf('facebook.com') >= 0 || this.$t("forms.rules.mustBeURL"),

        // isEmail: v => regexIsEmail(v) || this.$t("forms.rules.mustBeEmail"),
        // isCountry: v => this.isCountry(v) || this.$t("forms.rules.mustBeCountry"),
        // isKnowledgeArea: v => this.isKnowledgeArea(v) || this.$t("forms.rules.mustBeKnowledgeArea"),
        // minlen: v =>
        //   v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
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

    setTimeout(() => {
      this.$refs.form.validate()
    }, 500);

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

    kaName(knowledgeArea){
      return `[${knowledgeArea.code}] ${this.$t(knowledgeArea.name)}`
    },

    loadStructure: function(){
      let loadedStructure = cloneDeep(this.structure)
      // Transform attributes to be compatible with Form
      loadedStructure.managers = (loadedStructure.managers || []).map(id => this.user(id))
      loadedStructure.knowledge_areas = (loadedStructure.knowledge_areas || []).map(id => this.knowledgeArea(id))

      return loadedStructure
    },

    saveImage: async function(image_url) {
      try{
        await this.$store.dispatch("structure/update", {id:this.structure.id, image_url})
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
      let structure = cloneDeep(this.editedStructure);
      structure.managers = structure.managers.map(u => u.id)

      // In the case of no id, send event to parent to create structure
      if(!structure.id){
        this.$emit("create", structure)
        // re-enable button after 2 seconds
        setTimeout(()=>{ this.processing = false }, 2000)
        return
      }

      // Map knowledge areas
      structure.knowledge_areas = structure.knowledge_areas.map(u => u.id)

      try{
        await this.$store.dispatch("structure/update", structure)
        this.$store.dispatch("toast/success", this.$t('forms.toasts.saveSuccess'))

        // Reload structure to get updated IDS
        if(structure.id){
          await this.$store.dispatch("structure/load", [structure.id])
          this.editedStructure = this.loadStructure()
        }

      } catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t('forms.toasts.saveFailure'),
          error
        })
      }

      this.processing = false

    },

    localizedCountryName(country){
      let locale = this.$i18n.locale
      return country.translations[locale] || country.name
    },

    isCountry(value){
      // If no value enter, is valid
      if(!value) return true;
      // If random string entered, not valid
      if(!value.name) return false;

      // Compare entered
      value = this.localizedCountryName(value)
      let names = this.Countries.map(this.localizedCountryName)
      let isCountry = names.indexOf(value)
      return isCountry > -1
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