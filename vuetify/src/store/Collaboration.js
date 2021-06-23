import { CollaborationResource } from "../plugins/resource";

const Resource = CollaborationResource

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
    load: async function (context, payload) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => Resource.get({id})))
        items = items.map(i => i.body)
        context.commit("SET_MAP", items)

      }else{
        // No ids provided, just get list of all
        let params = payload.params || {}
        let query = {...params}

        let response = (await Resource.get(query)).body
        let items = response.results

        context.commit("SET", items)
      }
      // if (!ids){
      //   // No ids provided, just get list of all
      //   let items = (await CollaborationResource.get()).body.results
      //   context.commit("SET", items)
      // }else{
      //   // Ids provided, get detailed information on given pids
      //   let items = (await Promise.all(
      //     ids.map(id => CollaborationResource.get({id}) )
      //   ))
      //   items = items.map(i => i.body)
      //   items.map(item => context.commit("SET_MAP", {id:item.id, item}))
      // }
    },

    create: async function (context, object){
      let result = (await Resource.save(object))
      return result
    },

    update: async function (context, object){
      let result = (await Resource.update({id:object.id}, object))
      context.dispatch("load")
      context.dispatch("load", [object.id])
    },

    delete: async function (context, id){
      let result = (await Resource.delete({id}))
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
