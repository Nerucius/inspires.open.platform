export default {
  namespaced: true,

  state: {
    preferences: {
      lang: localStorage["lang"] || "en",
      theme: localStorage["theme"] || "light",
    },
  },

  mutations: {
    SET_PREFERENCE(state, pref) {
      let prefName = Object.keys(pref)[0]
      let prefValue = pref[prefName]
      state.preferences[prefName] = prefValue
      localStorage[prefName] = prefValue;
    },
    DEL_PREFERENCE(state, key) {
      delete state.preferences[key];
      localStorage.removeItem(key)
    }
  },

  actions: {
    set: function (context, pref) {
      context.commit("SET_PREFERENCE", pref);
    },
    delete: function (context, key) {
      context.commit("DEL_PREFERENCE", key);
    },
  },

  getters: {
    theme: state => {
      return state.preferences.theme;
    },
    lang: state => {
      return state.preferences.lang;
    },
  }
};