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



            <v-flex xs12 pa-0></v-flex>

            <v-flex md3 class="hidden-sm-and-down">
              <v-img src="/img/branding/inspires.png" />
            </v-flex>

            <v-flex sm12 md8>
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
                @keyup.native.enter="valid && submitLogin()"
                @submit.prevent="submitLogin()"
              >
                <v-text-field
                  v-model="credentials.username"
                  prepend-icon="person"
                  :label="$t('forms.fields.username')"
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
              </v-form>

            </v-flex>
          </v-layout>
        </v-card-text>
        <v-card-actions class="mt-2 pb-3 px-3 text-xs-center" >
          <v-flex shrink>
            <v-btn :to="{name:'register'}" dark flat outline color="primary">
              Register now!
            </v-btn>
          </v-flex>
          <v-spacer />
          <v-flex shrink>
            <v-btn :disabled="!valid" color="primary" @click="submitLogin()">
              {{ $t("actions.login") }}
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
  components: {
    LanguageSelector
  },

  data() {
    return {
      failedLogin: false,
      valid: null,
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
    // Avoid showing this page if the user is logged in
    if (this.isLoggedIn){
      this.redirectToPage();
    }
  },

  methods: {
    submitLogin() {
      if (this.$refs.form.validate()) {
        this.failedLogin = false;
        this.attemptLogin();
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
        let path = this.$route.query.redirect || "/";
        path = path == "/login" ? "/" : path
        this.$router.replace({ path });
    }
  }
};
</script>
