import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import i18n from './plugins/i18n';
import "./plugins/vuetify"
import "./plugins/matomo"
import "./plugins/filters";
import "./plugins/markdown";
import "./plugins/resource";
import "./registerServiceWorker";
import "./plugins/flagicon";


Vue.config.productionTip = false;


export default new Vue({
  router,
  store,
  i18n,
  mounted: () => document.dispatchEvent(new Event('x-app-rendered')),

  render: h => h(App),
}).$mount("#app");
