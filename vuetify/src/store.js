import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

// Global store utils

window.onlyUnique = function(value, index, self) {
  return self.indexOf(value) === index;
}
window.slug = function(id, value) {
  let slug = id+'-'+value.toString()
    .substring(0,40)
    .replace(/\s/g, "-")
    .toLowerCase()
  return encodeURI(slug)
}
window.slug2id = function(slug) {
  return slug.split('-')[0]
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