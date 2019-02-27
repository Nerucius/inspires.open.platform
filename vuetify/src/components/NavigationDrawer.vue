<style scoped>
  .subheading{
    line-height: 120%
  }

  .sidebar-header{
    background-image: url("http://www.outdoorphotographer.com/images/gallery/full/871/107871.jpg");
    background-size: cover;
    color:snow;
  }
  .sidebar-header small{
    color:lightgray
  }
</style>


<template>
  <v-navigation-drawer app v-model="showDrawer">
    <v-layout column justify-start fill-height>

      <v-flex class="pa-2 pt-3 px-4 sidebar-header" shrink>
          <v-flex>
            <v-avatar size="80">
              <img
                :src="`https://www.gravatar.com/avatar/${'205e460b479e2e5b48aec07710c08d50'}?s=256`"
                alt="avatar"
              >
            </v-avatar>
          </v-flex>
          <v-flex class="mt-3 subheading">
            <v-layout>
              <v-flex>
              {{ currentUser.first_name || "Anonymous" }}<br>
              <small>{{ currentUser.email || "anonymous@campus.edu" }}</small>
              </v-flex>
              <v-flex shrink class="py-1">
                  <v-icon dark @click="toggleAccountMenu()">
                    {{showAccountMenu ? 'keyboard_arrow_up' : 'keyboard_arrow_down'}}
                  </v-icon>
              </v-flex>
            </v-layout>
          </v-flex>

      </v-flex>

      <v-flex shrink>
        <v-list>
          <v-list-tile :to="{name:'home'}" exact>
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>Home Page</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile :to="{name:'courses'}" exact>
            <v-list-tile-action>
              <v-icon>view_agenda</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ $t("navigation.courses") }}</v-list-tile-title>
          </v-list-tile>

          <v-list-tile :to="{name:'calendar'}" exact>
            <v-list-tile-action>
              <v-icon>calendar_today</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ $t("navigation.calendar") }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-flex>

      <v-divider></v-divider>

      <v-spacer></v-spacer>

      <v-divider></v-divider>
      <v-flex shrink>
        <ThemeSelector/>
      </v-flex>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
import ThemeSelector from "@/components/drawer/ThemeSelector";

export default {
  name: "NavigationDrawer",

  components: {
    ThemeSelector
  },

  data() {
    return {
      showDrawer: null,
      showAccountMenu: false,
    };
  },

  methods: {
    toggleDrawer() {
      this.showDrawer = !this.showDrawer;
    },
    toggleAccountMenu() {
      this.showAccountMenu = !this.showAccountMenu;
    },
  },

  computed: {
    currentUser() {
      return this.$store.getters["user/current"];
    }
  }
};
</script>