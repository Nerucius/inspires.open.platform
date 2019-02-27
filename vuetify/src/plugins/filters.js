import Vue from "vue"
import i18n from "./i18n"

Vue.filter('capitalize', value => {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.filter('uppercase', value => {
  if (!value) return ''
  value = value.toString()
  return value.toUpperCase()
})

Vue.filter('ellipsis', (value, maxChars) => {
  value = value.toString()
  if (value.length < maxChars) return value
  return value.substring(0, maxChars-3) + '...'
})

Vue.filter('localize', value => {
    return i18n.t(value)
})

Vue.filter('md5', value => {
    return value
})
