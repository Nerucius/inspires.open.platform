import { AttachmentResource, ContentTypeResource } from "../plugins/resource";

const Resource = AttachmentResource

/** Function called on every object on load */
export function handle(obj){
  return obj
}

export default {
  namespaced: true,

  state: {
    itemsDetail: {},
    contentTypes: [],
  },

  mutations: {
    
    ADD_DETAIL(state, items) {
        let newItems = {}
        items.map(handle).forEach(i => {newItems[i.id] = i})
        state.itemsDetail = { ...state.itemsDetail, ...newItems }
    },

    ADD_CONTENTYPES(state, items){
        state.contentTypes = items;
    },

    CLEAR(state){
      state.itemsDetail = []
    },

    REMOVE(state, id){
      delete state.itemsDetail[id]
    }
  },

  actions: {
    load: async function (context, payload) {
      if (!!payload && Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => Resource.get({id})))
        items = items.map(i => i.body)
        context.commit("ADD_DETAIL", items)
      }else{
        console.error('Object does not support load all: Attachment');
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
      context.commit("REMOVE", id)
      return result
    },

    loadContentTypes: async function(context, _){
        let response = await ContentTypeResource.get();
        context.commit("ADD_CONTENTYPES", response.body.results)
    },
  },

  getters: {
    detail: state =>{
      return ( id ) => state.itemsDetail[id] || {}
    },

    contentType: state =>{
      return ( model ) => state.contentTypes.filter(ct => ct.model==model)[0]
    },
  }
};
