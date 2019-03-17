import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

import preferences from "./store/Preferences";
import user from "./store/User";
import project from "./store/Project";
import structure from "./store/Structure";
import collaboration from "./store/Collaboration";
import participation from "./store/Participation";

// CRUD Models

// Create Store
export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",
  modules: {
    preferences,
    user,
    project,
    structure,
    collaboration,
    participation
  }
});