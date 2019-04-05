import Vue from "../plugins/resource";
import Cookies from "js-cookie";
import {
  API_SERVER,
  UserResource,
  CurrentUserResource,
} from "../plugins/resource";


const userLoginUrl = API_SERVER + "/api-token-auth/";
const userRegisterUrl = API_SERVER + "/user/register/";

export default {
  namespaced: true,

  state: {
    current: null,
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

    SET_CURRENT(state, item){
      state.current = item
    }
  },

  actions: {
    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => UserResource.get({id})))
        items = items.map(i => i.body)
        context.commit("SET_DETAIL_ALL", items)

      }else{
        context.dispatch("loadCurrent")
        // No ids provided, just get list of all
        let params = payload.params || {}
        let query = {...params}

        let response = (await UserResource.get(query)).body
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

    loadCurrent: async function (context) {
      try{
        let user = (await CurrentUserResource.get()).body.results[0];
        context.commit("SET_CURRENT", user);
      }catch(err){
        // no auth
        context.commit("SET_CURRENT", null)
      }
    },

    login: async function (context, credentials) {
      return new Promise(async (resolve, reject) => {
        try {
          let authentication = (await Vue.http.post(userLoginUrl, credentials))
          let token = authentication.body.token
          Cookies.set('authorization', token)
          await context.dispatch("loadCurrent");
          resolve();

        } catch (err) {
          console.log(err)
          // Failed to login
          reject();
        }
      })
    },

    logout: async function (context) {
      // await Vue.http.get(userLogoutUrl);
      Cookies.remove('authorization')
      await context.dispatch("loadCurrent");
    },

    register: async function(context, newUser){
      return new Promise(async (resolve, reject) => {
        try {
          // await Vue.http.get(userRegisterUrl, {params: {...newUser}});
          await Vue.http.post(userRegisterUrl, newUser, {
            emulateJSON: true
          });
          // await context.dispatch("loadCurrent");
          resolve();

        } catch (err) {
          // Failed to register
          reject();
        }
      })
    }
  },

  getters: {
    all: state => {
      return Object.values(state.items)
    },

    get: state =>{
      return ( id ) => (state.items[id] || {})
    },

    detail: state =>{
      return ( id ) => (state.itemsDetail[id] || {})
    },

    current: state => {
      return state.current || {
        id: -1,
        first_name: "Anonymous",
        last_name: "",
        email: ""
      };
    },

    isLoggedIn: state => {
      return state.current != null && state.current.id > 0;
    }
  }
};