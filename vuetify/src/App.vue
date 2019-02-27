<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.1s;
  transition-property: opacity;
  transition-timing-function: ease;
}

.fade-enter,
.fade-leave-active {
  opacity: 0
}
</style>


<template>
  <v-app :[theme]="true">
    <template v-if="loading">
      <v-content>
        <v-container fill-height>
          <v-layout align-center justify-center>
            <v-flex xs12 class="text-xs-center">
              <v-btn fab large outline loading />
            </v-flex>
          </v-layout>
        </v-container>
      </v-content>
    </template>

    <template v-else>
      <!-- Navigation Drawer -->
      <NavigationDrawer v-if="shouldShowNavigation" ref="navigationDrawer" />
      <Toolbar ref="toolbar" :show-toggle-drawer="shouldShowNavigation" @toggleDrawer="toggleDrawer()" />
      <!-- Content -->
      <v-content>
        <v-container grid-list-xl fill-height>
          <transition
            name="fade"
            mode="out-in"
          >
            <router-view />
          </transition>

          <!-- <router-view :key="$route.fullPath"></router-view> -->
        </v-container>
      </v-content>
    </template>
  </v-app>
</template>

<script>
import NavigationDrawer from "@/components/NavigationDrawer";
import Toolbar from "@/components/Toolbar";
import { USE_REQUIRED_AUTH } from "@/router";

export default {
  name: "App",
  components: {
    NavigationDrawer,
    Toolbar
  },

  data() {
    return {
      loading: true
    };
  },

  computed: {
    theme() {
      return this.$store.getters["preferences/theme"];
    },
    shouldShowNavigation(){
      return this.$store.getters['user/isLoggedIn']
    },
  },

  async mounted() {
    // Block on the user status before allowing to show the app
    await this.$store.dispatch("user/load");
    this.loading = false;
  },

  methods: {
    toggleDrawer() {
      this.$refs.navigationDrawer.toggleDrawer();
    }
  }
};
</script>
