import { ProjectResource } from "../plugins/resource";
import { cloneDeep } from "lodash";

export default {
  namespaced: true,

  state: {
    items: [],
    itemMap: {},
  },

  mutations: {
    SET(state, items) {
      state.items = items;
    },
    SET_MAP(state, {id, item}) {
      state.itemMap = { ...state.itemMap, [id]:item }
    },
  },

  actions: {
    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => ProjectResource.get({id})))
        items = items.map(i => i.body)
        items.map(item => context.commit("SET_MAP", {id:item.id, item}))

      }else{
        // No ids provided, just get list of all
        let query = {ordering: "-modified_at", ...(payload.params || {})}
        let items = (await ProjectResource.get(query)).body.results
        context.commit("SET", items)
      }
    },

    create: async function (context, object){
      let result = await ProjectResource.save(object)
      let project = result.body
      await context.dispatch("load", [project.id])
      return project
    },

    update: async function (context, object){
      let result = (await ProjectResource.update({id:object.id}, object))
      context.dispatch("load")
      context.dispatch("load", [object.id])
    },
  },

  getters: {
    all: state => {
      return state.items
    },

    get: state =>{
      return ( id ) => cloneDeep(state.items.filter(item => item.id == id)[0] || {})
    },

    detail: state =>{
      return ( id ) => cloneDeep(state.itemMap[id] || {})
    },

  }
};