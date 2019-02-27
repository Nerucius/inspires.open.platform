<template>
  <v-toolbar scroll-off-screen app dark flat color="teal">
    <v-toolbar-side-icon v-if="showToggleDrawer" @click="$emit('toggleDrawer')" />
    <v-toolbar-title class="headline text-uppercase">
      <span>InSPIRES</span>&nbsp;
      <span style="font-size:70%" class="font-weight-light">
        Open Platform
      </span>
    </v-toolbar-title>
    <v-spacer />

    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn exact :to="{name:'home'}" flat>
        Home
      </v-btn>
      <v-btn exact :to="{path:'/projects'}" flat>
        Projects
      </v-btn>
      <v-divider vertical />
    </v-toolbar-items>

    <LanguageSelector />
    <LoginLogoutButton />
    <!-- <LoginDialog/> -->
  </v-toolbar>
</template>

<script>
import LoginLogoutButton from "@/components/toolbar/LoginLogoutButton";
import LanguageSelector from "@/components/toolbar/LanguageSelector";

export default {
  components: {
    LoginLogoutButton,
    LanguageSelector
  },

  props: ["showToggleDrawer"],

  computed: {
    userIsLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    }
  },

  methods: {
    getCourses() {
      this.$router.push("/courses");
    },
    getCalendar() {}
  }
};
</script>
