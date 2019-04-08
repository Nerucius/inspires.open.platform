import Vue from "../plugins/resource";
import { KnowledgeAreaResource } from "../plugins/resource";
import { cloneDeep } from "lodash";

export default {
  namespaced: true,

  state: {
    items: {},
  },

  mutations: {
    SET_ALL(state, items){
      let newItems = {}
      items.forEach(i => {newItems[i.id] = i})
      state.items = { ...state.items, ...newItems}
    },
  },

  actions: {
    load: async function (context, payload={}) {
        let response = (await KnowledgeAreaResource.get()).body
        let items = response.results

        // Iteratively get all pages
        let next = response.next
        while(next){
          response = (await Vue.http.get(next)).body
          items = [...items, ...response.results]
          next = response.next
        }

        context.commit("SET_ALL", items)
    },

  },

  getters: {
    all: state => {
      return Object.values(state.items)
    },

    get: state =>{
      return ( id ) => cloneDeep(state.items[id] || {})
    },

  }
};