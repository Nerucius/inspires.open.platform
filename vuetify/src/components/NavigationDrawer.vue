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

            <!-- Disabled account info toggle -->
            <!-- <v-flex shrink class="py-1">
              <v-icon dark @click="toggleAccountMenu()">
                {{ showAccountMenu ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}
              </v-icon>
            </v-flex> -->
          </v-layout>
        </v-flex>
      </v-flex>

      <!-- Account Menu DISABLED -->
      <!-- <v-flex v-if="showAccountMenu" shrink>
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
      </v-flex> -->

      <!-- User Menu -->
      <v-flex v-if="!showAccountMenu" shrink>
        <v-expansion-panel class="elevation-0" focusable>
          <v-expansion-panel-content>
            <!-- Trigger Slot -->
            <template v-slot:header>
              <v-layout py-2 align-center="">
                <v-flex pr-3 shrink>
                  <v-icon size="28" style="flex-shrink:1">
                    person
                  </v-icon>
                </v-flex>
                <v-flex class="subheading">
                  {{ $t("toolbar.myProjects") }}
                </v-flex>
              </v-layout>
            </template>

            <v-list>
              <v-list-tile to="/projects/1">
                <v-list-tile-title>Project Alpha</v-list-tile-title>
              </v-list-tile>
              <v-list-tile to="/projects/2">
                <v-list-tile-title>Project Beta</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-divider />

        <v-expansion-panel class="elevation-0" focusable>
          <v-expansion-panel-content>
            <!-- Trigger Slot -->
            <template v-slot:header>
              <v-layout py-2 align-center="">
                <v-flex pr-3 shrink>
                  <v-icon size="28" style="flex-shrink:1">
                    person
                  </v-icon>
                </v-flex>
                <v-flex class="subheading">
                  {{ $t("toolbar.myStructures") }}
                </v-flex>
              </v-layout>
            </template>

            <v-list>
              <v-list-tile>
                <v-list-tile-title>Project Alpha</v-list-tile-title>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-title>Project Beta</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-divider />

        <!--
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

          <v-list-tile :to="{name:'account'}" exact>
            <v-list-tile-action>
              <v-icon>public</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ $t("navigation.commissioners") }}</v-list-tile-title>
          </v-list-tile>
          -->
      </v-flex>


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