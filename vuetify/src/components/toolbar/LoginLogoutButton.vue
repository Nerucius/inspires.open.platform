<template>
  <v-btn v-if="!isLoggedIn" flat :to="{name:'login'}">
    {{ $t('actions.login') }}
    <v-icon right>
      lock_open
    </v-icon>
  </v-btn>

  <v-btn v-else flat @click="logout()">
    {{ $t('actions.logout') }}
    <v-icon right>
      exit_to_app
    </v-icon>
  </v-btn>
</template>


<script>
export default {
  name:"LoginLogoutButton",

  computed: {
    isLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    },
  },

  methods:{
    logout(){
      this.$store.dispatch("user/logout")
    }
  }
}
</script>
