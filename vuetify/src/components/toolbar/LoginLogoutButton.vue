<template>
  <v-btn v-if="!isLoggedIn" flat :to="{name:'login'}">
    {{ $t('actions.login') }}
    <v-icon right>
      lock_open
    </v-icon>
  </v-btn>

  <!-- <v-btn v-else flat @click="logout()">
    {{ $t('actions.logout') }}
    <v-icon right>
      exit_to_app
    </v-icon>
  </v-btn>-->

  <v-menu v-else offset-y>
    <v-btn slot="activator" flat>
      {{ user.first_name }}
      <v-icon right>
        expand_more
      </v-icon>
    </v-btn>
    <v-list>
      <v-list-tile v-if="user.is_administrator" :to="{name:'administration'}">
        <v-list-tile-title>
          {{ $t('toolbar.administration') }}
        </v-list-tile-title>
      </v-list-tile>

      <v-list-tile :to="{name:'account'}">
        <v-list-tile-title>
          {{ $t('toolbar.myAccount') }}
        </v-list-tile-title>
      </v-list-tile>

      <v-divider />

      <v-list-tile @click="logout()">
        <v-list-tile-title>
          Log out
          <v-icon right>
            exit_to_app
          </v-icon>
        </v-list-tile-title>
      </v-list-tile>
    </v-list>
  </v-menu>
</template>


<script>
export default {
  name: "LoginLogoutButton",

  computed: {
    isLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    },
    user() {
      return this.$store.getters["user/current"];
    }
  },

  methods: {
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$store.dispatch("toast/info", this.$t('forms.toasts.loggedOut'));
      this.$router.push({ name: 'home'})
    }
  }
};
</script>
