<style>
  /* Global Styles */
  /* Link text underline for list links */
  .container .v-list a{ text-decoration: none; }
  .container .v-list a:hover{ text-decoration: underline; }

    /* html{overflow-y:auto} */
  ::-webkit-scrollbar {
    width: 5px;
    background: teal;
    /*display: inline !important;*/
  }
  #toast-container {padding-top: 10px}
  .v-snack { padding-top: 10px; }
</style>

<style scoped>
  /* Transitions */
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
      <NavigationDrawer
        v-if="shouldShowNavigation"
        ref="navigationDrawer"
      />
      <Toolbar
        ref="toolbar"
        :show-toggle-drawer="shouldShowNavigation"
        @toggleDrawer="toggleDrawer()"
      />
      <!-- Content -->
      <v-content>
        <v-container grid-list-xl fill-height>
          <!-- Main Content Area -->
          <transition
            name="fade"
            mode="out-in"
          >
            <router-view :key="routePathKey" />
          </transition>
          <!-- /Main Content Area -->
        </v-container>

        <!-- Footer Area -->
        <v-container>
          <v-layout row>
            <v-flex xs12>
              <Footer />
            </v-flex>
          </v-layout>
        </v-container>
        <!-- /Footer Area -->

        <!-- Snackbars -->
        <v-snackbar
          v-for="toast in toasts"
          :key="toast.key"
          v-model="toast.active"
          auto-height
          top
          :color="toast.color"
          :timeout="toast.timeout"
        >
          {{ toast.message }}
          <v-btn dark flat fab @click="toast.close()">
            <v-icon>close</v-icon>
          </v-btn>
        </v-snackbar>
        <!-- /Snackbars -->
      </v-content>
    </template>
  </v-app>
</template>

<script>
import NavigationDrawer from "@/components/NavigationDrawer";
import Toolbar from "@/components/Toolbar";
import Footer from "@/components/Footer";

export default {
  name: "App",
  components: {
    NavigationDrawer,
    Toolbar,
    Footer,
  },

  metaInfo:{
    title: "InSPIRES Platform",
    titleTemplate: '%s | InSPIRES',
  },

  data() {
    return {
      loading: true,
      active: true,
    };
  },

  computed: {
    toasts(){
      return this.$store.getters['toast/all']
    },
    theme() {
      return this.$store.getters["preferences/theme"];
    },
    shouldShowNavigation(){
      return this.$store.getters['user/isLoggedIn']
    },
    routePathKey(){
      // Returns a usable fullRoute key without the hash to use as in-page state
      return this.$route.fullPath.replace(/#.*/gi, '')
    }
  },

  async created() {
    // setTimeout(() => {
    //   document.dispatchEvent(new Event('x-app-rendered'))
    // }, 1000)

    // Block on the user status before allowing to show the app
    await this.$store.dispatch("user/load");
    this.loading = false;

    // Trigger SSR
    setTimeout(()=>{
      document.dispatchEvent(new Event('x-app-rendered'))
    }, 100)
  },

  methods: {
    toggleDrawer() {
      this.$refs.navigationDrawer.toggleDrawer();
    }
  }
};
</script>
