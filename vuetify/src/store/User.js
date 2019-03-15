import Vue from "../plugins/resource";
import {
  API_SERVER,
  UserResource,
  CurrentUserResource,
  refreshCSRFCookie,
} from "../plugins/resource";


const userLoginUrl = API_SERVER + "/user/login/";
const userLogoutUrl = API_SERVER + "/user/logout/";
const userRegisterUrl = API_SERVER + "/user/register/";

export default {
  namespaced: true,

  state: {
    current: null,
    items: [],
    itemMap: {},
  },

  mutations: {
    SET_CURRENT(state, user) {
      state.current = user;
    },
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
        context.dispatch("loadCurrent")
        let items = (await UserResource.get()).body.results
        context.commit("SET", items)
      }else{
        // Ids provided, get detailed information on given pids
        let items = (await Promise.all(
          ids.map(id => ProjectResource.get({id}) )
        ))
        items = items.map(i => i.body)
        items.map(item => context.commit("SET_MAP", {id:item.id, item}))
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

    get: async function(context, userIds){
      let users = await Promise.all(
        userIds.map(id => UserResource.get({id}) )
      )
      users = users.map(u => u.body[0])
      return users
    },

    login: async function (context, credentials) {
      return new Promise(async (resolve, reject) => {
        try {
          await Vue.http.post(userLoginUrl, credentials, {
            emulateJSON: true
          });
          await refreshCSRFCookie();
          await context.dispatch("loadCurrent");
          resolve();

        } catch (err) {
          // Failed to login
          reject();
        }
      })
    },

    logout: async function (context) {
      await Vue.http.get(userLogoutUrl);
      await refreshCSRFCookie();
      await context.dispatch("loadCurrent");
    },

    register: async function(context, newUser){
      return new Promise(async (resolve, reject) => {
        try {
          await Vue.http.post(userRegisterUrl, newUser, {
            emulateJSON: true
          });
          await refreshCSRFCookie();
          await context.dispatch("loadCurrent");
          resolve();

        } catch (err) {
          // Failed to login
          reject();
        }
      })
    }
  },

  getters: {
    all: state =>{
      return state.items
    },

    get: state =>{
      return ( id ) => state.items.filter(item => item.id == id)[0] || {}
    },

    detail: state =>{
      return ( id ) => state.itemMap[id] || {}
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