import Vue from "../plugins/resource";
import { API_SERVER} from "../plugins/resource";


/** Generate unique random key for each toast */
const key = function(){
  return Math.random().toString(36).replace(/[^a-z]+/g, '').substr(2, 10);
}

const isObject = function (val) {
  if (val === null) { return false;}
  return ( (typeof val === 'function') || (typeof val === 'object') );
}

export default {
  namespaced: true,

  state: {
    toasts: []
  },

  mutations: {
    ADD_TOAST(state, toast) {
      // state.toasts = [...state.toasts, toast]
      // Disable multiple toasts for now, latest is always on top
      state.toasts = [toast]
    },
    REMOTE_TOAST(state, key) {
      state.toasts = state.toasts.filter( t => t.key != key)
    }
  },

  actions: {
    new: function(context, toast){
      let toastKey = key()
      toast = {
        ...toast,
        timeout: 5000,
        key: toastKey,
        close: () => context.commit("REMOTE_TOAST", toastKey)
      }
      context.commit("ADD_TOAST", toast)
      setTimeout(toast.close, toast.timeout)
    },

    info: function (context, message) {
      context.dispatch("new", {color:"info", message});
    },
    success: function (context, message) {
      context.dispatch("new", {color:"success", message});
    },
    error: function (context, params) {
      let message = params
      let error
      if(isObject(params)) {
        message = params.message
        error = params.error
      }
      context.dispatch("new", {color:"error", message});
      context.dispatch("logError", {message, error});
    },

    logError: async function(context, {message, error}){
      if (error) error = JSON.stringify(error)
      else error = "";
      let user = context.rootGetters["user/current"].id
      Vue.http.get(`${API_SERVER}/v1/log-error`, {params:{message, user, error}})
    }
  },

  getters: {
    all: state => {
      return state.toasts.map(toast => ({...toast, active:true}))
    }
  }
};