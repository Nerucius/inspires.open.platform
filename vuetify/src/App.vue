<style>
  /* Global Styles */

  ::-webkit-scrollbar {
      width: 0.65em;
  }

  ::-webkit-scrollbar-track {
    margin-top: -1px;
    background: rgb(12, 77, 77);
      /* -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); */
  }

  ::-webkit-scrollbar-thumb {
    background:#00796b;
    border-top: 1px solid lightgray;
    border-bottom: 1px solid lightgray;
  }

  #toast-container {padding-top: 10px}
  .v-snack { padding-top: 10px; }

  hr {
    border: 0;
    border-top: 1px solid rgb(12, 77, 77);
    height: 0px;
  }
</style>

<style>
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

  .list-enter-active, .list-leave-active {
    transition: all 0.5s;
  }
  .list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
    opacity: 0;
}
</style>


<template>
  <v-app :[theme]="true" @setLanguage="checkRTL($event)">
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
        <v-container id="footer">
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
          style="z-index:999999"
        >
          <span v-html="toast.message" />
          <v-btn dark flat fab @click="toast.close()">
            <v-icon>close</v-icon>
          </v-btn>
        </v-snackbar>
        <!-- /Snackbars -->
      </v-content>

      <!-- Cookie Policy Toast -->
      <CookieToast />
    </template>
  </v-app>
</template>

<script>
import NavigationDrawer from "@/components/NavigationDrawer";
import CookieToast from "@/components/CookieToast";
import Toolbar from "@/components/Toolbar";
import Footer from "@/components/Footer";

import { setI18nLanguage } from "@/plugins/i18n";

export default {
  name: "App",
  components: {
    CookieToast,
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
      // TODO: completely disabled navigation drawer
      return false;

      // return this.$store.getters['user/isLoggedIn']
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

    // Listener for language selection
    this.$store.subscribe((mutation, state) => {
      if(mutation.type == 'preferences/SET_PREFERENCE'
        && mutation.payload.hasOwnProperty('lang')){

        let lang = mutation.payload.lang
        this.$vuetify.rtl = lang == 'ar';

        console.log('Language Change request: '+ lang)
        setI18nLanguage(lang);

      }
    });

    // Trigger SSR
    setTimeout(()=>{
      document.dispatchEvent(new Event('x-app-rendered'))
    }, 100)
  },

  methods: {
    toggleDrawer() {
      this.$refs.navigationDrawer.toggleDrawer();
    },
  }
};
</script>
