import { FeedbackResource } from "../plugins/resource";

const Resource = FeedbackResource

/** Function called on every object on load */
export function handle(obj){
  return obj
}

export default {
  namespaced: true,

  state: {
  },

  mutations: {
  },

  actions: {
    create: async function (context, object){
      let newItem = (await Resource.save(object)).body
      return newItem
    },
  },

  getters: {
  }
};
