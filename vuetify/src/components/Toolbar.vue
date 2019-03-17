<template>
  <v-toolbar scroll-off-screen app dark flat color="primary">
    <v-toolbar-side-icon v-if="showToggleDrawer" @click="$emit('toggleDrawer')" />
    <v-toolbar-title class="headline text-uppercase">
      <span>InSPIRES</span>&nbsp;
      <span style="font-size:70%" class="font-weight-light">
        Open Platform
      </span>
    </v-toolbar-title>
    <v-spacer />

    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn v-for="link in links" :key="link.name"
             flat
             exact
             :to="{name:link.name}"
      >
        {{ $t(link.label) }}
      </v-btn>

      <v-divider vertical />

      <LanguageSelector />
      <LoginLogoutButton />
    </v-toolbar-items>

    <v-menu bottom left class="hidden-md-and-up">
      <v-btn slot="activator" large dark icon>
        <v-icon>more_vert</v-icon>
      </v-btn>

      <v-list>
        <v-list-tile v-for="link in links" :key="link.name" exact :to="{name:link.name}">
          {{ $t(link.label) }}
        </v-list-tile>
        <v-divider />

        <v-list-tile v-if="!userIsLoggedIn" exact :to="{name:'login'}">
          {{ $t("actions.login") }}
        </v-list-tile>
        <v-list-tile v-else @click="logout()">
          {{ $t("actions.logout") }}
        </v-list-tile>
      </v-list>
    </v-menu>
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

  data(){
    return{
      links: [
        {name: "home", label:"navigation.links.home"},
        {name: "project-list", label:"navigation.links.projects"}
      ]
    }
  },

  computed: {
    userIsLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    }
  },

  methods: {
    getCourses() {
      this.$router.push("/courses");
    },
    getCalendar() {},
    logout() {
      this.$store.dispatch("user/logout")
      this.$router.push({name:'home'});
    }
  }
};
</script>
