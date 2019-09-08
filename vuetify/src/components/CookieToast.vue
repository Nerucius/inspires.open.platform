<style scoped>

  a{
    color:lightgreen;
  }
  p{
    margin: 0
  }

</style>


<template>
  <v-snackbar
    v-model="showToast"
    auto-height
    :timeout="0"
  >
    <p>
      {{ $t('pages.legal.cookieToast') }}
      <router-link :to="{name:'cookie-policy'}">
        {{ $t('actions.moreInformation') }}.
      </router-link>
    </p>

    <v-btn dark color="success" @click="acceptCookies()">
      {{ $t('actions.accept') }}
    </v-btn>
  </v-snackbar>
</template>


<script>
import Cookies from "js-cookie";

export default {

  data() {
    return {
      showToast: false,
    }
  },

  mounted() {
    let cookiesAccepted = Cookies.get('accept-cookies', false)

    if (!cookiesAccepted){
      this.showToast = true;
    }
  },

  methods: {
    acceptCookies(){
      Cookies.set('accept-cookies', true, { expires: 365 })
      this.showToast = false;
    }
  },

}
</script>