<style>
  /* Remove top textarea margin (too big textarea box) */
  textarea{
    margin-top: 6px !important
  }
</style>

<template>
  <div>
    <v-form v-model="valid" ref="form" @submit="attemptSubmit">

      <template v-if="!submitted">
        <p class="subheading">
          {{ $t("pages.about.contactUsContent") }}
        </p>

        <v-text-field
          v-model="feedback.email"
          :placeholder="$t('misc.optional')"
          :disabled="submitted"
          :label="$t('forms.fields.email')"
          outline
        />
        <v-textarea
          v-model="feedback.text"
          :disabled="submitted"
          :rules="[rules.required]"
          outline
        />
      </template>

      <v-btn
        v-if="!submitted"
        block
        large
        color="success"
        :disabled="!valid || processing"
        :loading="processing"
        type="submit"
      >
        {{ $t("actions.submit") }}
      </v-btn>

      <v-btn
        v-else
        block
        large
        color="success"
        disabled="disabled"
      >
        {{ $t("pages.help.courses.feedbackSubmitted") }}
      </v-btn>

    </v-form>

    <div v-if="currentUser.is_administrator" class="py-2">
      <v-btn color="error" outline block target="_blank" :href="feedbackAdminURL">
        View all Feedback (Admin)
      </v-btn>
    </div>


  </div>
</template>

<script>
import { API_SERVER } from "@/plugins/resource";

export default {
  props: ["model", "objectId", "title", "feedbackType"],

  data() {
    return {
      feedback: {
        rating: null,
        text: "",
      },
      valid: false,
      processing: false,
      submitted : false,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
    };
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
    feedbackAdminURL(){
      return `${API_SERVER}/admin/backend/feedback`
    }
  },

  async created(){
    // Load content types
    await this.$store.dispatch('attachment/loadContentTypes');
  },

  methods: {

    async attemptSubmit(e) {
      e.preventDefault();
      if(!this.valid || this.submitted)
        return;

      // Copy email to body
      if(!!this.feedback.email)
        this.feedback.text = `contact: ${this.feedback.email}\n\n${this.feedback.text}`

      // Complete feedback object
      var feedbackData = {
        ...this.feedback,
        feedback_type: this.feedbackType,
      }

      // Add user info
      if(this.$store.getters['user/isLoggedIn']){
        feedbackData = {
          ...feedbackData,
          user: this.currentUser.id,
        }
      }

      // Attempt to save
      try {
        this.processing = true;
        await this.$store.dispatch("feedback/create", feedbackData);
        this.$store.dispatch("toast/success", this.$t("pages.help.courses.feedbackSubmitted"));
        this.submitted = true

      } catch (error) {
        this.$store.dispatch("toast/error", {message: this.$t("forms.toasts.saveFailure"), error,});
      }
      this.processing = false;
    },
  },
};
</script>

<style>
</style>
