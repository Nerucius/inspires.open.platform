import Vue from "../plugins/resource";
import Cookies from "js-cookie";
import {
  API_SERVER,
  UserResource,
  CurrentUserResource,
  CUEvaluationsResource,
} from "../plugins/resource";
import { obj2slug } from "../plugins/utils";

export const GROUP_USER = 1
export const GROUP_ADMIN = 2

const userLoginUrl = API_SERVER + "/api-token-auth/";
const userRegisterUrl = API_SERVER + "/user/register/";
const userResetPasswordRequestUrl = API_SERVER + "/user/resetpassword/";
const userResetPasswordSubmitUrl = API_SERVER + "/user/resetpasswordsubmit/";

function createLink(obj){
  obj.link = {name:"account", params:{slug:obj2slug(obj, 'full_name')}}
  obj.form_name = `${obj.full_name} (${obj.username})`
  return obj
}

export default {
  namespaced: true,

  state: {
    current: null,
    items: {},
    itemsDetail: {},

    genders: [
      {value:"", name:"misc.notSpecified"},
      {value:"MALE", name:"models.userGender.male"},
      {value:"FEMALE", name:"models.userGender.female"},
      {value:"OTHER", name:"models.userGender.other"},
    ],

    educationLevels : [
      {value:"", name:"misc.notSpecified"},
      {value:"PRIMARY", name: "models.educationLevel.primary"},
      {value:"SECONDARY", name: "models.educationLevel.secondary"},
      {value:"TERTIARY", name: "models.educationLevel.tertiary"},
      {value:"DEGREE", name: "models.educationLevel.degree"},
      {value:"MASTER", name: "models.educationLevel.master"},
      {value:"DOCTORAL", name: "models.educationLevel.doctoral"},
    ]
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

    SET_CURRENT(state, item){
      state.current = item
    },

    SET_CURRENT_EVALUATIONS(state, items){
      state.current = {...state.current, evaluations: items}
    }
  },

  actions: {
    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => UserResource.get({id})))
        items = items.map(i => i.body)
        context.commit("ADD_DETAIL", items)

      }else{
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

        context.commit("ADD", items)
      }
    },

    loadCurrent: async function (context) {
      try{
        let response = await CurrentUserResource.get()
        let user = response.body.results[0]
        context.commit("SET_CURRENT", user);
        context.commit("ADD_DETAIL", [user]);
      }catch(err){
        // no auth
        console.log("Authentication not found. User not logged in")
        Cookies.remove('authorization')
        context.commit("SET_CURRENT", null)
      }
    },

    loadCurrentEvaluations: async function(context) {
      try{
        let response = await CUEvaluationsResource.get()
        let evaluations = response.body.results
        context.commit("SET_CURRENT_EVALUATIONS", evaluations);
      }catch(err){ }
    },

    login: async function (context, credentials) {
        let authentication = (await Vue.http.post(userLoginUrl, credentials))
        let token = authentication.body.token
        Cookies.set('authorization', token, {sameSite:"Strict"})
        await context.dispatch("loadCurrent");
    },

    resetPassword: async function (context, credentials) {
        let response = await Vue.http.post(
          userResetPasswordRequestUrl, credentials, {emulateJSON: true}
        )
    },

    resetPasswordSubmit: async function (context, credentials) {
        let response = await Vue.http.post(
          userResetPasswordSubmitUrl, credentials, {emulateJSON: true}
        )
    },

    logout: async function (context) {
      // await Vue.http.get(userLogoutUrl);
      Cookies.remove('authorization')
      await context.dispatch("loadCurrent");
    },

    updateCurrent: async function(context, user){
      let changed = (await UserResource.update({id:user.id}, user)).body
      context.commit("SET_CURRENT", changed)
      return changed
    },

    register: async function(context, newUser){
      // await Vue.http.get(userRegisterUrl, {params: {...newUser}});
      let response = await Vue.http.post(userRegisterUrl, newUser, { emulateJSON: true })
      return response.body
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
      return ( id ) => state.itemsDetail[id]
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
    },

    educationLevels: state => state.educationLevels,
    genders: state => state.genders,
  }
};
