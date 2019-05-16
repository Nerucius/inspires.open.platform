import Vue from "../plugins/resource";
import { ProjectResource } from "../plugins/resource";
import { cloneDeep } from "lodash";
import { obj2slug } from "@/plugins/utils";

const Resource = ProjectResource

function createLink(obj){
  obj.link = {name:"project-detail", params:{slug:obj2slug(obj)}}
  obj.image_url = obj.image_url || "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg"
  return obj
}

export default {
  namespaced: true,

  state: {
    items: {},
    itemsDetail: {},

    projectTypes: [
      {value:"RESEARCH",                        name: "models.projectType.research"},
      {value:"PARTICIPATORY_RESEARCH",          name: "models.projectType.participatoryResearch"},
      {value:"PARTICIPATORY_ACTION_RESEARCH",   name: "models.projectType.participatoryActionResearch"},
      {value:"CITIZEN_SCIENCE",                 name: "models.projectType.citizenScience"},
      {value:"PUBLIC_ENGAGEMENT",               name: "models.projectType.publicEngagement"},
      {value:"SERVICE_LEARNING",                name: "models.projectType.serviceLearning"},
      {value:"ADVOCACY",                        name: "models.projectType.advocacy"},
      {value:"INNOVATION",                      name: "models.projectType.innovation"},
      {value:"POLICY_INNOVATION",               name: "models.projectType.policyInnovation"},
      {value:"OTHER",                           name: "models.projectType.other"},
    ],

  },

  mutations: {
    ADD(state, items){
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.id] = i})
      state.items = { ...state.items, ...newItems}
    },

    ADD_DETAIL(state, items) {
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.id] = i})
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
        let query = {ordering: "-modified_at", ...params}

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

    search: async function (context, params) {
      let query = {ordering: "-modified_at", ...params}

      let response = (await Resource.get(query)).body
      let items = response.results

      // Iteratively get all pages
      let next = response.next
      while(next){
        response = (await Vue.http.get(next)).body
        items = [...items, ...response.results]
        next = response.next
      }

      return items.map(createLink)
    },

    clear: function(context, _){
      context.commit("CLEAR")
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

    projectTypes: state => state.projectTypes,
  }
};