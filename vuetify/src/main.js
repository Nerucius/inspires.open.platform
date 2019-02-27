import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import i18n from './plugins/i18n';
import './plugins/vuetify'
import "./plugins/filters";
import "./plugins/resource";
import "./registerServiceWorker";
import FlagIcon from "vue-flag-icon";

Vue.use(FlagIcon);

Vue.config.productionTip = false;

export default new Vue({
  router,
  store,
  i18n,
  mounted: () => document.dispatchEvent(new Event('x-app-rendered')),
  render: h => h(App), // Prerender SPA
}).$mount("#app");