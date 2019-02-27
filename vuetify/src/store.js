import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

import preferences from "./store/Preferences";
import user from "./store/User";

// CRUD Models

// Create Store
export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",
  modules: {
    preferences,
    user,
  }
});