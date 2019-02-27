import Vue from "../plugins/resource";
import {
  API_SERVER,
  UserResource,
  CurrentUserResource,
  refreshCSRFCookie,
} from "../plugins/resource";


const userLoginUrl = API_SERVER + "/user/login/";
const userLogoutUrl = API_SERVER + "/user/logout/";

export default {
  namespaced: true,

  state: {
    user: null,
    users: [],
  },

  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
  },

  actions: {
    load: async function (context) {
      try{
        let user = (await CurrentUserResource.get()).body[0];
        context.commit("SET_USER", user);
      }catch(err){
        // no auth
        context.commit("SET_USER", null)
      }
    },

    login: async function (context, credentials) {
      return new Promise(async (resolve, reject) => {
        try {
          await Vue.http.post(userLoginUrl, credentials, {
            emulateJSON: true
          });
          await refreshCSRFCookie();
          await context.dispatch("load");
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
      await context.dispatch("load");
    }
  },

  getters: {
    current: state => {
      if (state.user) return state.user;
      return {
        pk: -1,
        first_name: "Anonymous",
        last_name: "",
        email: ""
      };
    },

    isLoggedIn: state => {
      return state.user != null && state.user.pk > 0;
    }
  }
};