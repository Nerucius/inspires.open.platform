import Vue from "../plugins/resource";
import { ContentResource } from "../plugins/resource";

const Resource = ContentResource

export function createLink(obj){
  // Help articles (standalone)
  if(obj.type == 'HELP')
    obj.link = {name:"help-article", params:{page:obj.slug}}
  // eLearning Courses
  if(obj.type == 'COURSE' || obj.type == 'MODULE')
    obj.link = {name:"help-course", params:{page:obj.slug}}
  // News
  if(obj.type == 'NEWS')
    obj.link = {name:"news", params:{page:obj.slug}}
  // Blog
  if(obj.type == 'BLOG')
    obj.link = {name:"blog", params:{page:obj.slug}}

  obj.topic = obj.topic.toLowerCase()

  return obj
}

export default {
  namespaced: true,

  state: {
    items: {},
    itemsDetail: {},

    articleTypes: [
        {value:"HELP",name: "models.content.types.HELP"},
        {value:"NEWS",name: "models.content.types.NEWS"},
        {value:"BLOG",name: "models.content.types.BLOG"},
    ],

  },

  mutations: {
    ADD(state, items){
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.slug] = i})
      state.items = { ...state.items, ...newItems}
    },

    ADD_DETAIL(state, items) {
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.slug] = i})
      state.itemsDetail = { ...state.itemsDetail, ...newItems }
    },

    CLEAR(state){
      state.items = []
      state.itemsDetail = []
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
        let items = await Promise.all(ids.map(id => Resource.get({id})))
        items = items.map(i => i.body)
        context.commit("ADD_DETAIL", items)

      }else{
        // No ids provided, just get list of all
        let params = payload.params || {}
        let query = {...params}

        let response = (await Resource.get(query)).body
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

    clear: function(context, _){
      context.commit("CLEAR")
    },

    // create: async function (context, object){
    //   let newItem = (await Resource.save(object)).body
    //   await context.dispatch("load", [newItem.id])
    //   return newItem
    // },

    // update: async function (context, object){
    //   let updatedItem = (await Resource.update({id:object.id}, object)).body
    //   context.commit("ADD_DETAIL", [updatedItem])
    //   return updatedItem
    // },

    // delete: async function (context, id){
    //   let result = (await Resource.delete({id}))
    //   context.dispatch("delete", id)
    //   return result
    // },

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

    projectTypes: state => state.projectTypes,
  }
};
