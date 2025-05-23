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
      counter="400"
      :label="$t('forms.fields.summary')"
      :hint="$t('forms.hints.structureSummary')"
    />

    <v-textarea
      v-if="editedStructure.id"
      v-model="editedStructure.description"
      box
      rows="16"
      :label="$t('forms.fields.description')"
      :hint="$t('forms.hints.description')"
    />

    <v-select
      v-model="editedStructure.structure_type"
      box
      :rules="[rules.required]"
      :items="$store.getters['structure/structureTypes']"
      :item-text="e => $t(e.name)"
      :label="$t('forms.fields.structureType')"
      :hint="$t('forms.hints.structureType')"
    />

    <v-text-field
      v-model="editedStructure.year_founded"
      box
      type="number"
      :rules="[rules.required, rules.validYear]"
      :label="$t('forms.fields.structureYearFounded')"
    />

    <div class="mb-4" />

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
      <div class="mb-4" />

      <h2 class="mt-4 mb-2">
        {{ $t('pages.projectManage.infoAdditionalTitle') }}
      </h2>

      <v-combobox ref="countriesCB"
                  v-model="editedStructure.country_code"
                  box multiple
                  chips deletable-chips
                  :items="Countries"
                  :item-text="countryTL"
                  item-value="alpha3Code"
                  :rules="[rules.isCountry]"
                  :label="$t('forms.fields.structureCountry')"
                  :hint="$t('forms.hints.structureCountry')"
                  @input="clearSearch('countriesCB')"
      />

      <template>
        <h3 class="mb-2">
          {{ $t('forms.fields.networks') }}
        </h3>

        <p class="subheading">{{ $t('forms.hints.networks') }}</p>

        <v-combobox
          ref="networksCB"
          v-model="editedStructure.networks"
          box
          :label="$t('forms.fields.networks')"
          :hint="$t('forms.hints.networks')"
          multiple
          chips
          deletable-chips
          :rules="[rules.isUser]"
          :items="$store.getters['network/all']"
          item-text="name"
          item-value="id"
          @input="clearSearch('networksCB')"
        />
      </template>


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
        :rules="[rules.isUser]"
        :items="$store.getters['knowledgearea/all']"
        :item-text="knowledgeAreaTL"
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

      <h2 class="mb-2">
        {{ $t('pages.projectManage.infoContactTitle') }}
      </h2>

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
        isEmail: v => true,
        required: v => !!v || this.$t("forms.rules.requiredField"),
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        isURL: v => regexIsURL(v) || this.$t("forms.rules.mustBeURL"),
        isTwitter: v => !v || v.indexOf('twitter.com') >= 0 || this.$t("forms.rules.mustBeURL"),
        isFacebook: v => !v || v.indexOf('facebook.com') >= 0 || this.$t("forms.rules.mustBeURL"),
        isCountry: v => this.isCountry(v) || this.$t("forms.rules.mustBeCountry"),
        validYear: v => !v || (v >= 500 && v <= 2100) || this.$t("forms.rules.mustBeValidYear"),
      },
      userSearch: [],
      editedStructure: {},

    };
  },

  computed:{
  },

  async created() {
    this.$store.dispatch("knowledgearea/load")

    if (this.structure && this.structure.id) {
      // Editing existing structure
      this.editedStructure = this.loadStructure()

      // Validate form in case required fields have changed
      setTimeout(() => {this.$refs.form.validate()}, 1000);

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

    knowledgeAreaTL(knowledgeArea){
      return `[${knowledgeArea.code}] ${this.$t(knowledgeArea.name)}`
    },

    loadStructure: function(){
      let loadedStructure = cloneDeep(this.structure)

      // Transform attributes to be compatible with Form
      loadedStructure.managers = (loadedStructure.managers || []).map(id => this.user(id))
      loadedStructure.knowledge_areas = (loadedStructure.knowledge_areas || []).map(id => this.knowledgeArea(id))
      loadedStructure.networks = (loadedStructure.networks || []).map(this.$store.getters['network/get'])

      // Countries string to objects
      loadedStructure.country_code = loadedStructure.country_code.split(',').map(cc =>
        this.Countries.filter(c => c.alpha3Code == cc)[0]
      ).filter(i => i != undefined)

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
      if(structure.country_code != null){
        structure.country_code = structure.country_code.map(c => c.alpha3Code).join()
      }

      // In the case of no id, send event to parent to create structure
      if(!structure.id){
        this.$emit("create", structure)
        // re-enable button after 2 seconds
        setTimeout(()=>{ this.processing = false }, 2000)
        return
      }

      // Map knowledge areas
      structure.knowledge_areas = structure.knowledge_areas.map(u => u.id)
      structure.networks = structure.networks.map(u => u.id)

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

    isCountry(values){
      return values.every(v => v.hasOwnProperty('alpha3Code'))
    },

    countryTL(country){
      let locale = this.$i18n.locale
      return country.translations[locale] || country.name
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
