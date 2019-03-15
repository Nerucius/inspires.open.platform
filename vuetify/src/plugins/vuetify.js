// Material design icons
import '@mdi/font/css/materialdesignicons.css'

import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import i18n from './i18n';
import theme from './vuetify.theme'



// Import i18n to translate Vuetify's text

Vue.use(Vuetify, {
  iconfont: 'mdi',
  theme,
  lang: {
    t: (key, ...params) => i18n.t(key, params)
  },
})