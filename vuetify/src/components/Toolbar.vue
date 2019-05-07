<style scoped>
.v-toolbar__title .router-link{
  color:inherit;
  text-decoration: inherit;
}
.v-toolbar__title .router-link:hover{
  background-color: rgba(255,255,255,0.1)
}
</style>


<template>
  <v-toolbar scroll-off-screen app dark flat color="primary">
    <v-toolbar-side-icon v-if="showToggleDrawer" @click="$emit('toggleDrawer')" />
    <v-toolbar-title class="headline text-uppercase">
      <router-link :to="{name:'home'}" active-class="router-link">
        <span style="text-transform:none">
          InSPIRES
        </span>
        <span style="font-size:70%" class="font-weight-light hidden-sm-and-down">
          &nbsp; Open Platform
        </span>
      </router-link>
    </v-toolbar-title>
    <v-spacer />

    <v-flex>
      <v-text-field
        class="pa-0"
        color="grey lighten-3"
        hide-details
        single-line
        prepend-icon="search"
        browser-autocomplete="off"
        :placeholder="$t('toolbar.searchPlaceholder')"
        />
    </v-flex>

    <v-spacer />

    <v-toolbar-items class="hidden-md-and-down">

      <!-- Full width items -->
      <v-btn v-for="link in links.filter(l => !l.miniOnly)"
          flat exact
          :key="link.name"
          :to="{name:link.name}"
      >
        {{ $t(link.label) }}
      </v-btn>

      <v-divider vertical />

      <LanguageSelector />

      <v-divider vertical />

      <LoginLogoutButton />
    </v-toolbar-items>

    <!-- SM devices links -->
    <v-menu bottom left class="hidden-lg-and-up">
      <v-btn slot="activator" large dark icon>
        <v-icon>more_vert</v-icon>
      </v-btn>

      <v-list>

        <template v-for="(link,idx) in links" >
          <v-list-tile v-if="!link.divider"
            :key="link.name" exact :to="{name:link.name}">
            {{ $t(link.label) }}
          </v-list-tile>

        <v-divider v-else :key="idx" />

        </template>

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
      menuLinks: [
        {name: "home", label:"navigation.links.home"},
        {name: "project-list", label:"noums.projects"},
        {name: "structure-list", label:"noums.structures"},
      ]
    }
  },

  computed: {
    links(){
      if(this.userIsLoggedIn){
        return [
          {miniOnly: true, name:"account", label: this.currentUser.first_name},
          {miniOnly: true, divider:true},
          ...this.$data.menuLinks,
        ]
      }
      return this.menuLinks;
    },
    userIsLoggedIn() {
      return this.$store.getters["user/isLoggedIn"];
    },
    currentUser(){
      return this.$store.getters["user/current"]
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
