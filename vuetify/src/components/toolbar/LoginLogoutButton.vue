<template>

    <v-btn v-if="!isLoggedIn" flat :to="{name:'login'}">
      {{ $t('actions.login') }}
      <v-icon right>person</v-icon>
    </v-btn>

    <v-btn v-else flat @click="logout()">
      {{ $t('actions.logout') }}
      <v-icon right>exit_to_app</v-icon>
    </v-btn>

</template>


<script>
export default {
  name:"LoginLogoutButton",

  methods:{
    logout(){
      this.$store.dispatch("user/logout")
    }
  },

  computed: {
    isLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    },
  }
}
</script>
