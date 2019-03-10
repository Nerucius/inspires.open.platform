import { StructureResource } from "../plugins/resource";

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
        let items = (await StructureResource.get({ordering: "-modified_at"})).body.results
        context.commit("SET", items)
      }else{
        // Ids provided, get detailed information on given pids
        let items = (await Promise.all(
          ids.map(id => StructureResource.get({id}) )
        ))
        items = items.map(i => i.body)
        items.map(item => context.commit("SET_MAP", {id:item.id, item}))
      }
    },
  },

  getters: {
    all: state => {
      return state.items
    },

    get: state =>{
      return ( id ) => state.items.filter(item => item.id == id)[0] || {}
    },

    detail: state =>{
      return ( id ) => state.itemMap[id] || {}
    },

  }
};