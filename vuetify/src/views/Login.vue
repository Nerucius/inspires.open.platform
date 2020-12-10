<template>
  <v-layout row justify-center>
    <v-flex xs12 md10 lg8 xl6>
      <v-card class="elevation-12">
        <v-toolbar dense flat dark color="primary">
          <v-toolbar-title>{{ $t('forms.titles.login') }}</v-toolbar-title>
          <v-spacer />
          <v-toolbar-items>
            <LanguageSelector />
          </v-toolbar-items>
        </v-toolbar>

        <v-card-text>
          <!-- <div class="text-xs-center mb-3">
            <h1 class="title">{{ $t("pages.login.welcomeMessage") }}</h1>
          </div> -->

          <!-- Logo -->
          <v-layout row wrap justify-space-around align-center px-2>
            <v-flex xs12 pa-0 />

            <v-flex md3 class="hidden-sm-and-down">
              <v-img src="/img/branding/inspires.png" />
            </v-flex>

            <!-- Form to login with credentials -->
            <v-flex v-if="!resetPassword" md8>
              <v-alert
                :value="failedLogin"
                dismissible
                type="error"
                class="my-3"
              >
                {{ $t("forms.errors.invalidCredentials") }}
              </v-alert>

              <v-form
                ref="form"
                v-model="valid"
                @submit.prevent="submitLogin()"
              >
                <v-text-field
                  v-model="credentials.username"
                  prepend-icon="person"
                  :label="$t('forms.fields.usernameOrEmail')"
                  :rules="rules"
                  type="text"
                />
                <v-text-field
                  v-model="credentials.password"
                  prepend-icon="lock"
                  :label="$t('forms.fields.password')"
                  :rules="rules"
                  type="password"
                />

                <v-layout wrap justify-space-between>
                  <v-flex shrink>
                    <v-btn outline @click="resetPassword = true">
                      {{ $t("pages.login.forgotPassword") }}
                    </v-btn>
                  </v-flex>
                  <v-flex shrink>
                    <v-btn type="submit" :disabled="!valid" color="primary">
                      {{ $t("actions.login") }}
                    </v-btn>
                  </v-flex>
                </v-layout>
              </v-form>
            </v-flex>

            <!-- Form to reset password -->
            <v-flex v-else md8>
              <v-alert
                :value="resetPasswordSubmitted"
                type="info"
                class="my-3"
              >
                {{ $t("forms.toasts.resetPasswordSubmitted") }}
              </v-alert>

              <v-form
                ref="formResetPassword"
                v-model="validResetPassword"
                @submit.prevent="submitResetPassword()"
              >
                <v-text-field
                  v-model="credentials.username"
                  prepend-icon="person"
                  :label="$t('forms.fields.usernameOrEmail')"
                  :rules="rules"
                  type="text"
                />
              </v-form>

              <v-layout mt-5 wrap justify-space-between>
                <v-flex shrink>
                  <v-btn outline @click="resetPassword = false">
                    {{ $t("pages.resetPassword.goBackToLogin") }}
                  </v-btn>
                </v-flex>
                <v-flex shrink>
                  <v-btn type="submit" :disabled="!validResetPassword || resetPasswordSubmitted" color="primary">
                    {{ $t("pages.resetPassword.resetPassword") }}
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions class="mt-2 pb-3 px-3 text-xs-center">
          <v-flex v-if="!resetPassword" shrink>
            <v-btn :to="{name:'register'}" dark flat outline color="primary">
              {{ $t('pages.login.registerCTA') }}
            </v-btn>
          </v-flex>
          <v-spacer />

          <!-- <v-flex v-if="!resetPassword" shrink>
            <v-btn :disabled="!valid" color="primary" @click="submitLogin()">
              {{ $t("actions.login") }}
            </v-btn>
          </v-flex>
          <v-flex v-else shrink>
            <v-btn :disabled="!validResetPassword || resetPasswordSubmitted" color="primary" @click="submitResetPassword()">
              {{ $t("pages.resetPassword.resetPassword") }}
            </v-btn>
          </v-flex> -->
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import Cookies from "js-cookie";
import LanguageSelector from "@/components/toolbar/LanguageSelector";

export default {
  metaInfo(){
    return {
      title: this.$t("forms.titles.login")
    }
  },

  components: {
    LanguageSelector
  },

  data() {
    return {
      failedLogin: false,
      resetPassword: false,
      resetPasswordSubmitted: false,
      valid: null,
      validResetPassword: null,
      credentials: {
        username: "",
        password: ""
      },
      rules: [v => !!v || this.$t("forms.rules.requiredField")],
    };
  },

  computed: {
    isLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    },
  },

  mounted(){

    // Autologin
    if(this.$route.query.token){
      Cookies.set('authorization', this.$route.query.token, {sameSite:"Strict"});
      this.$store.dispatch('user/load')
      this.redirectToPage();
    }

    // Avoid showing this page if the user is logged in
    setTimeout(() => {
      if (this.isLoggedIn){
        this.redirectToPage();
      }
    }, 500);
  },

  methods: {
    submitLogin() {
      if (this.$refs.form.validate()) {
        this.failedLogin = false;
        this.attemptLogin();
      }
    },

    async submitResetPassword() {
      if (this.$refs.formResetPassword.validate()) {
        try{
          await this.$store.dispatch("user/resetPassword", this.credentials)
          this.resetPasswordSubmitted = true

        }catch(error){
          this.$store.dispatch("toast/error", {
            message: this.$t('pages.login.resetPasswordError'),
            error
          })
        }


      }
    },

    attemptLogin() {
      // Send the credentials to be logged in and redirect to the
      // next page if successful

      this.$store.dispatch("user/login", this.credentials)
      .then(()=>{
        this.redirectToPage();
      })
      .catch(err => {
        // this.$refs.form.reset();
        this.credentials.password = ''
        this.failedLogin = true;
      });
    },

    redirectToPage(){
        // Redirect to requested route before force login
        // or homepage if landed on login
        let path = this.$route.query.redirect || "/account";
        path = path == "/login" ? "/" : path
        this.$router.push({ path });
    }
  }
};
</script>
