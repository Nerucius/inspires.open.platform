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
  <v-toolbar scroll-off-screen app dark flat color="primary" style="z-index:999">
    <v-toolbar-side-icon v-if="showToggleDrawer" @click="$emit('toggleDrawer')" />
    <v-toolbar-title class="headline text-uppercase">
      <router-link :to="{name:'home'}" active-class="router-link">
        <span style="text-transform:none">
          InSPIRES
        </span>
        <span style="font-size:70%" class="font-weight-light hidden-md-and-down">
          &nbsp; Open Platform
        </span>
      </router-link>
    </v-toolbar-title>
    <v-spacer />

    <v-flex>
      <v-form ref="searchForm" @submit.prevent="search()">
        <v-text-field
          v-model="searchTerm"
          class="pa-0 ma-0 px-1"
          color="grey lighten-3"
          hide-details
          single-line
          prepend-icon="search"
          browser-autocomplete="off"
          :rules="[rules.minimunLength]"
          :placeholder="$t('actions.search')"
        />
      </v-form>
    </v-flex>

    <v-spacer />

    <!-- Desktop toolbar items -->
    <v-toolbar-items class="hidden-sm-and-down">
      <!-- Full width items -->
      <v-btn v-for="link in links.filter(l => !l.miniOnly)"
             :key="link.name" flat
             :exact="link.name == 'home'"
             :to="{name:link.name}"
      >
        {{ $t(link.label) }}
      </v-btn>

      <v-divider vertical />

      <LanguageSelector />

      <v-divider vertical />

      <LoginLogoutButton />
    </v-toolbar-items>

    <!-- Mobile toolbar links -->
    <v-toolbar-items class="hidden-md-and-up">
      <LanguageSelector />
      <v-menu bottom left>
        <v-btn slot="activator" large dark icon>
          <v-icon>more_vert</v-icon>
        </v-btn>

        <v-list class="pa-0">
          <template v-for="(link,idx) in links">
            <v-list-tile v-if="!link.divider"
                         :key="link.name" exact :to="{name:link.name}"
            >
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
    </v-toolbar-items>
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
      searchTerm: "",
      menuLinks: [
        {name: "home", label:"navigation.links.home"},
        // {name: "help", label:"navigation.links.help"},
        {name: "project-list", label:"noums.projects"},
        {name: "structure-list", label:"noums.structures"},
        {name:"help", label: "navigation.links.learn"}
      ],
      rules: {
        minimunLength: v => (!v || v.length >= 3) || this.$t("forms.rules.minimunLength", {'length':3}),
      }
    }
  },

  computed: {
    links(){
      if(this.userIsLoggedIn){
        let links = [
          {miniOnly: true, name:"account", label: this.currentUser.first_name}
        ]
        // Admin Panel Link
        if(this.currentUser.is_administrator){
          links.push({miniOnly: true, divider:true})
          links.push({miniOnly: true, name:"administration", label: "Administration"})
        }

        links.push({miniOnly: true, divider:true})
        links.push(...this.$data.menuLinks)

        return links
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

  created() {
    this.searchTerm = this.$route.query['term']
  },

  methods: {
    search(){
      if(this.$refs.searchForm.validate()){
        this.$router.push({name:"search", query:{q:this.searchTerm}})
      }
    },
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
