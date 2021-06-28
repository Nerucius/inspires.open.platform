<style>
  /* Remove top textarea margin (too big textarea box) */
  textarea{
    margin-top: 6px !important
  }
</style>

<template>
  <div>
    <!-- White header -->
    <v-sheet color="white" class="pa-3">
      <h1 class="title">{{ $t("pages.help.courses.feedbackTitle") }}</h1>
    </v-sheet>

    <!-- Gray textbox -->
    <v-sheet class="grey lighten-4 pa-3">
      <p class="subheading">
        {{ $t("pages.help.courses.feedbackLabelStars") }}
      </p>

      <v-form ref="form" @submit="attemptSubmit">

        <!-- Rating feedback -->
        <v-layout my-3 wrap justify-center align-center>
          <v-flex ma-0 shrink class="title">
            {{ title }}
          </v-flex>
          <v-flex ma-0 pa-0 shrink>
            <v-rating
              v-model="feedback.rating"
              color="yellow darken-3"
              :rules="[rules.required]"
              :disabled="submitted"
              large
              background-color="grey darken-1"
              empty-icon="$vuetify.icons.ratingEmpty"
              hover
            />
          </v-flex>
        </v-layout>

        <template v-if="!submitted">
          <p class="subheading">
            {{ $t("pages.help.courses.feedbackLabelTextbox") }}
          </p>

          <v-textarea v-model="feedback.text" outline :disabled="submitted" />
        </template>

        <v-btn
          v-if="!submitted"
          block
          large
          color="success"
          :disabled="!isValid || processing"
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
    </v-sheet>

  </div>
</template>

<script>
export default {
  props: ["model", "objectId", "title", "feedbackType"],

  data() {
    return {
      feedback: {
        rating: null,
        text: "",
      },
      processing: false,
      submitted : false,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
    };
  },

  computed:{
    isValid(){
      return this.feedback.rating != null;
    },
    currentUser(){
      return this.$store.getters['user/current']
    },
  },

  async created(){
    // Load content types
    this.checkSubmitted();
    await this.$store.dispatch('attachment/loadContentTypes');
  },

  methods: {
    checkSubmitted(){
      var subData = JSON.parse(window.localStorage.getItem('feedback') || '{}')
      var key = `fb-${this.model}-${this.objectId}`
      // Check if exists and load rated value if so
      this.submitted = subData.hasOwnProperty(key)
      if(this.submitted)
        this.feedback.rating = subData[key]

    },

    saveSubmitted(){
      var subData = JSON.parse(window.localStorage.getItem('feedback') || '{}')
      var key = `fb-${this.model}-${this.objectId}`
      subData[key] = this.feedback.rating;
      window.localStorage.setItem('feedback', JSON.stringify(subData));
    },

    async attemptSubmit(e) {
      e.preventDefault();
      if(!this.isValid || this.submitted)
        return;

      // get contentType
      var contentType = this.$store.getters['attachment/contentType'](this.model).id;

      // Complete feedback object
      var feedbackData = {
        ...this.feedback,
        feedback_type: this.feedbackType,
        object_id: this.objectId,
        content_type: contentType,
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
        this.$store.dispatch("toast/success", this.$t("forms.toasts.saveSuccess"));
        this.submitted = true
        this.saveSubmitted()

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
