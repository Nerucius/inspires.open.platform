import Vue from "../plugins/resource";
import { NetworkResource } from "../plugins/resource";
import { handle as structureHandle } from "./Structure";

const Resource = NetworkResource

/** Function called on every object on load */
export function handle(obj){
  // Make links to all structures if this is a detail view
  try {
    obj.structures = obj.structures.map(s => structureHandle(s))
  } catch (_) {}
  return obj
}

export default {
  namespaced: true,

  state: {
    items: {},
    itemsDetail: {},
  },

  mutations: {
    ADD(state, items){
      let newItems = {}
      items.map(handle).forEach(i => {newItems[i.id] = i})
      state.items = { ...state.items, ...newItems}
    },

    ADD_DETAIL(state, items) {
      let newItems = {}
      items.map(handle).forEach(i => {newItems[i.id] = i})
      state.itemsDetail = { ...state.itemsDetail, ...newItems }
    },

    CLEAR(state){
      state.items = []
      state.itemsDetail = []
    },

    REMOVE(state, id){
      delete state.items[id]
      delete state.itemsDetail[id]
    }
  },

  actions: {
    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => Resource.get({id})))
        items = items.map(i => i.body)
        context.commit("ADD_DETAIL", items)

      }else{
        // No ids provided, just get list of all
        let params = payload.params || {}
        let query = {...params}

        let response = (await Resource.get(query)).body
        let items = response.results

        // Only get next pages if no parameters were set
        if(params.limit === undefined && params.offset === undefined){
          let next = response.next
          while(next){
            response = (await Vue.http.get(next)).body
            items = [...items, ...response.results]
            next = response.next
          }
        }

        context.commit("ADD", items)
      }
    },

    create: async function (context, object){
      let newItem = (await Resource.save(object)).body
      await context.dispatch("load", [newItem.id])
      return newItem
    },

    update: async function (context, object){
      let updatedItem = (await Resource.update({id:object.id}, object)).body
      context.commit("ADD_DETAIL", [updatedItem])
      return updatedItem
    },

    delete: async function (context, id){
      let result = (await Resource.delete({id}))
      context.dispatch("delete", id)
      return result
    },
  },

  getters: {
    all: state => {
      return Object.values(state.items)
    },

    get: state =>{
      return ( id ) => state.items[id] || {}
    },

    detail: state =>{
      return ( id ) => state.itemsDetail[id] || {}
    },
  }
};
