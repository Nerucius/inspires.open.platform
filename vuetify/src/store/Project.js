import Vue from "../plugins/resource";
import { ProjectResource } from "../plugins/resource";
import { cloneDeep } from "lodash";

export default {
  namespaced: true,

  state: {
    items: {},
    itemsDetail: {},
  },

  mutations: {
    ADD(state, items){
      let newItems = {}
      items.forEach(i => {newItems[i.id] = i})
      state.items = { ...state.items, ...newItems}
    },

    ADD_DETAIL(state, items) {
      let newItems = {}
      items.forEach(i => {newItems[i.id] = i})
      state.itemsDetail = { ...state.itemsDetail, ...newItems }
    },

    DELETE(state, id){
      delete state.items[id]
      delete state.itemsDetail[id]
    }
  },

  actions: {
    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => ProjectResource.get({id})))
        items = items.map(i => i.body)
        context.commit("ADD_DETAIL", items)

      }else{
        // No ids provided, just get list of all
        let params = payload.params || {}
        let query = {ordering: "-modified_at", ...params}

        let response = (await ProjectResource.get(query)).body
        let items = response.results

        // Iteratively get all pages
        let next = response.next
        while(next){
          response = (await Vue.http.get(next)).body
          items = [...items, ...response.results]
          next = response.next
        }

        context.commit("ADD", items)
      }
    },

    create: async function (context, object){
      let newItem = (await ProjectResource.save(object)).body
      await context.dispatch("load", [newItem.id])
      return newItem
    },

    update: async function (context, object){
      let updatedItem = (await ProjectResource.update({id:object.id}, object)).body
      context.commit("ADD_DETAIL", [updatedItem])
      return updatedItem
    },

    delete: async function (context, id){
      let result = (await ParticipationResource.delete({id}))
      context.dispatch("DELETE", id)
      return result
    },
  },

  getters: {
    all: state => {
      return Object.values(state.items)
    },

    get: state =>{
      return ( id ) => cloneDeep(state.items[id] || {})
    },

    detail: state =>{
      return ( id ) => cloneDeep(state.itemsDetail[id] || {})
    },

  }
};