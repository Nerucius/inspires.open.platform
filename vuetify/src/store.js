import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

// Global store utils

window.onlyUnique = function(value, index, self) {
  return self.indexOf(value) === index;
}
window.slug = function(id, value) {
  return id+'-'+value.toString().substring(0,30).toLowerCase().replace(/\s/g, "-")
}

import preferences from "./store/Preferences";
import user from "./store/User";
import project from "./store/Project";
import structure from "./store/Structure";

// CRUD Models

// Create Store
export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",
  modules: {
    preferences,
    user,
    project,
    structure,
  }
});