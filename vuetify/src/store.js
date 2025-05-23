import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

import preferences from "./store/Preferences";
import toast from "./store/Toast"

import user from "./store/User";
import project from "./store/Project";
import knowledgearea from "./store/KnowledgeArea";
import structure from "./store/Structure";
import network from "./store/Network";
import collaboration from "./store/Collaboration";

import content from "./store/Content";
import attachment from "./store/Attachment";
import feedback from "./store/Feedback";

import participation from "./store/Participation";
import evaluation from "./store/Evaluation";

// CRUD Models

// Create Store
export default new Vuex.Store({
  strict: process.env.NODE_ENV !== "production",
  modules: {
    preferences,
    toast,
    user,
    project,
    knowledgearea,
    structure,
    network,
    content,
    attachment,
    feedback,
    collaboration,
    participation,
    evaluation,
  }
});
