import { CollaborationResource } from "../plugins/resource";

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
    load: async function (context, ids) {
      if (!ids){
        // No ids provided, just get list of all
        let items = (await CollaborationResource.get()).body.results
        context.commit("SET", items)
      }else{
        // Ids provided, get detailed information on given pids
        let items = (await Promise.all(
          ids.map(id => CollaborationResource.get({id}) )
        ))
        items = items.map(i => i.body)
        items.map(item => context.commit("SET_MAP", {id:item.id, item}))
      }
    },

    create: async function (context, object){
      let result = (await CollaborationResource.save(object))
      return result
    },

    update: async function (context, object){
      let result = (await CollaborationResource.update({id:object.id}, object))
      context.dispatch("load")
      context.dispatch("load", [object.id])
    },

    delete: async function (context, id){
      let result = (await CollaborationResource.delete({id}))
      return result
    },
  },

  getters: {
    all: state => {
      return [...state.items]
    },

    get: state =>{
      return ( id ) => ({...state.items.filter(item => item.id == id)[0]}) || {}
    },

    detail: state =>{
      return ( id ) => ({...state.itemMap[id]}) || {}
    },

  }
};
