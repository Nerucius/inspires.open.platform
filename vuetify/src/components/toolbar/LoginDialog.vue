<template>
  <v-btn v-if="userIsLoggedIn" flat @click="logout()">
    {{ $t('actions.logout') }}
    <v-icon right>
      exit_to_app
    </v-icon>
  </v-btn>

  <v-dialog v-else max-width="450px">
    <v-btn slot="activator" flat @click="resetForm()">
      {{ $t('actions.login') }}
      <v-icon right>
        person
      </v-icon>
    </v-btn>

    <v-card class="">
      <v-toolbar dark color="primary" class="elevation-0">
        <v-toolbar-title>{{ $t('forms.titles.login') }}</v-toolbar-title>
        <v-spacer />
        <v-toolbar-items />
      </v-toolbar>

      <v-card-text>
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
            ref="usernameInput"
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
      </v-card-text>
      <v-card-actions class="pb-3 pr-3">
        <v-spacer />
        <v-btn :disabled="!valid" color="primary" @click="submitLogin()">
          {{ $t("actions.login") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      failedLogin: false,
      valid: null,
      credentials: {
        username: "",
        password: ""
      },
      rules: [v => !!v || this.$t("forms.rules.requiredField")]
    };
  },

  computed: {
    userIsLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    }
  },

  methods: {
    resetForm() {
      this.$refs.form.reset();
      // Focus username field after animation
      setTimeout(() => {
        this.$refs.usernameInput.focus();
      }, 100);
    },

    submitLogin() {
      if (this.$refs.form.validate()) {
        this.attemptLogin();
      }
    },

    attemptLogin() {
      this.$store.dispatch("user/login", this.credentials).catch(err => {
        this.$refs.form.reset();
        this.failedLogin = true;
      });
    },

    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push({ name: 'login' });
    }
  }
};
</script>
