<template>
  <v-layout row justify-center>
    <v-flex xs12 md10 lg8 xl6>
      <v-card class="elevation-12">
        <v-toolbar dense flat dark color="primary">
          <v-toolbar-title>{{ $t('pages.resetPassword.title') }}</v-toolbar-title>
          <v-spacer />
          <v-toolbar-items>
            <LanguageSelector />
          </v-toolbar-items>
        </v-toolbar>

        <v-card-text>
          <v-alert
            :value="passwordChanged"
            type="success"
            class="my-3"
          >
            {{ $t("pages.resetPassword.passwordChanged") }}
          </v-alert>


          <v-form v-if="!passwordChanged" ref="form" v-model="valid" @submit.prevent="submitResetPassword()">
            <p class="subheading my-3">
              {{ $t('pages.resetPassword.introText') }}
            </p>

            <v-text-field
              v-model="credentials.password"
              type="password"
              :label="$t('forms.fields.password')"
              :rules="[rules.required, rules.minimunLength, rules.passwordValid]"
              prepend-icon="lock"
              @input="$refs.form.validate()"
            />
            <v-text-field
              v-model="credentials.password2"
              type="password"
              :label="$t('forms.fields.passwordRepeat')"
              :rules="[rules.required, rules.passwordMatch]"
              prepend-icon="lock"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-flex shrink>
            <v-btn
              v-if="!passwordChanged"
              :disabled="!valid"
              color="primary"
              @click="submitResetPassword()"
            >
              {{ $t("pages.resetPassword.resetPassword") }}
            </v-btn>
            <v-btn
              v-else
              color="primary"
              :to="{name:'login'}"
            >
              {{ $t("pages.resetPassword.goBackToLogin") }}
            </v-btn>
          </v-flex>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import LanguageSelector from "@/components/toolbar/LanguageSelector";

export default {
  metaInfo(){
    return {
      title: this.$t("pages.resetPassword.title")
    }
  },

  components: {
    LanguageSelector
  },

  data() {
    return {
      passwordRequestError: false,
      passwordChanged: false,
      valid: null,
      credentials: {
        password: "",
        password2: ""
      },
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minimunLength: v =>
          (v || "").length >= 8 ||
          this.$t("forms.rules.minimunLength", { length: 8 }),
        passwordValid: v =>
          this.isValidPassword(v) || this.$t("forms.rules.passwordField"),
        passwordMatch: v =>
          this.credentials.password == this.credentials.password2 ||
          this.$t("forms.rules.passwordMatch")
      }
    };
  },

  computed: {
    isLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    }
  },

  mounted() {
    this.$store.dispatch("user/logout", false);
  },

  methods: {
    async submitResetPassword() {
      if (this.$refs.form.validate()) {
        this.credentials.token = this.$route.query.token

        try{
          await this.$store.dispatch('user/resetPasswordSubmit', this.credentials)
          this.passwordChanged = true;
        }catch(error){
          this.$store.dispatch("toast/error", {
            message: this.$t('pages.resetPassword.resetPasswordError'),
            error
          })
        }

      }
    },

    isValidPassword(value = "") {
      value = value.toLowerCase();
      return (
        true &&
        value != "12345678" &&
        value != "password" &&
        value != "password1" &&
        value != "password12" &&
        value != "password123" &&
        value != "password1234"
      );
    }
  }
};
</script>
