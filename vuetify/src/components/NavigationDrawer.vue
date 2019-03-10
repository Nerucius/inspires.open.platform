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

  .v-list > div{
    margin-bottom: 4px
  }
</style>


<template>
  <v-navigation-drawer v-model="showDrawer" app temporary>
    <v-layout column justify-start fill-height>
      <v-flex class="pa-2 pt-3 px-4 sidebar-header" shrink>
        <v-flex>
          <v-avatar size="80">
            <img
              :src="currentUser.avatar_url"
              alt="avatar"
            >
          </v-avatar>
        </v-flex>
        <v-flex class="mt-3 subheading">
          <v-layout>
            <v-flex>
              {{ currentUser.first_name }} {{ currentUser.last_name }} <br>
              <small>{{ currentUser.email }}</small>
            </v-flex>
            <v-flex shrink class="py-1">
              <v-icon dark @click="toggleAccountMenu()">
                {{ showAccountMenu ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}
              </v-icon>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-flex>

      <!-- Account Menu -->
      <v-flex v-if="showAccountMenu" shrink>
        <v-list>
          <v-list-tile :to="{name:'account'}" exact>
            <v-list-tile-action>
              <v-icon>person</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>My Account</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-flex>

      <v-divider />

      <!-- User Menu -->
      <v-flex v-if="!showAccountMenu" shrink>
        <v-list>
          <v-list-tile :to="{name:'my-dashboard'}" exact>
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>{{ $t("navigation.dashboard") }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-list-tile :to="{name:'account-projects'}" exact>
            <v-list-tile-action>
              <v-icon>work</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ $t("navigation.projects") }}</v-list-tile-title>
          </v-list-tile>

          <v-list-tile :to="{name:'account-structures'}" exact>
            <v-list-tile-action>
              <v-icon>school</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ $t("navigation.structures") }}</v-list-tile-title>
          </v-list-tile>

          <v-list-tile :to="{name:'account-commissioners'}" exact>
            <v-list-tile-action>
              <v-icon>public</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ $t("navigation.commissioners") }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-flex>

      <v-divider />

      <v-spacer />

      <v-divider />
      <v-flex shrink>
        <ThemeSelector />
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

  computed: {
    currentUser() {
      return this.$store.getters["user/current"];
    }
  },

  methods: {
    toggleDrawer() {
      this.showDrawer = !this.showDrawer;
    },
    toggleAccountMenu() {
      this.showAccountMenu = !this.showAccountMenu;
    },
  }
};
</script>