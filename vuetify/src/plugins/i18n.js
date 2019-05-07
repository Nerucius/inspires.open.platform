import Vue from 'vue'
import VueI18n from 'vue-i18n'
import Cookies from "js-cookie";


Vue.use(VueI18n)

export const ListOfLocales = []
// Load list of countries:
export const Countries = require("../locales/_countries.json")
// export const GeoJSONCountries = require("../locales/_geoJSONCountries.json")
export const GeoJSONCountriesDetail = require("../locales/_geoJSONCountries2.json")

function loadLocaleMessages() {
  const locales = require.context('../locales', true, /[A-Za-z0-9-_]+\.json$/i)
  const messages = {}
  locales.keys().forEach(key => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i)
    if (matched && matched.length > 1) {
      const locale = matched[1]

      // Locales are only valid if they are 2 characters
      if (locale.length != 2) { return }

      ListOfLocales.push(locale)
      messages[locale] = locales(key)
    }
  })
  return messages
}

const i18n = new VueI18n({
  locale: localStorage["lang"] || process.env.VUE_APP_I18N_LOCALE,
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages: loadLocaleMessages()
})

export function setI18nLanguage(lang) {
  if (ListOfLocales.indexOf(lang) < 0) {
    throw new Error(`Language not in list of locales: ${lang}`)
  }
  Cookies.set("lang", lang)
  if(i18n.locale == lang) {
      console.log("Ignored same language change")
      return
  }
  i18n.locale = lang
  document.querySelector('html').setAttribute('lang', lang)
  return lang
}

export default i18n;