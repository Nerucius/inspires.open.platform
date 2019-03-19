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
    SET(state, {id, item}) {
      state.items = { ...state.items, [id]:item }
    },

    SET_DETAIL(state, {id, item}) {
      state.itemsDetail = { ...state.itemsDetail, [id]:item }
    },

    SET_ALL(state, items){
      let newItems = {}
      items.forEach(i => {newItems[i.id] = i})
      state.items = { ...state.items, ...newItems}
    },

    SET_DETAIL_ALL(state, items) {
      let newItems = {}
      items.forEach(i => {newItems[i.id] = i})
      state.itemsDetail = { ...state.itemsDetail, ...newItems }
    },
  },

  actions: {
    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => ProjectResource.get({id})))
        items = items.map(i => i.body)
        context.commit("SET_DETAIL_ALL", items)

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

        context.commit("SET_ALL", items)
      }
    },

    create: async function (context, object){
      let newItem = (await ProjectResource.save(object)).body
      await context.dispatch("load", [newItem.id])
      return newItem
    },

    update: async function (context, object){
      let updatedItem = (await ProjectResource.update({id:object.id}, object))
      context.dispatch("load")
      context.dispatch("load", [object.id])
      return updatedItem
    },

    delete: async function (context, id){
      let result = (await ParticipationResource.delete({id}))
      context.dispatch("load")
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