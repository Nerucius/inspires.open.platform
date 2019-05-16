import Vue from "vue"
import i18n from "./i18n"

Vue.filter('capitalize', value => {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.filter('lowercase', value => {
  if (!value) return ''
  value = value.toString()
  return value.toLowerCase()
})

Vue.filter('uppercase', value => {
  if (!value) return ''
  value = value.toString()
  return value.toUpperCase()
})

Vue.filter('nlbr', value => {
  if (!value) return ''
  value = value.toString()
  return value.replace(/\n/g, "<br>")
})

Vue.filter('ellipsis', (value, maxChars, dots=true) => {
  if (!value) return ""

  value = value.toString()
  if (value.length < maxChars) return value
  if(dots)
    return value.substring(0, maxChars-3) + '...'
    else
    return value.substring(0, maxChars)
})

Vue.filter('localize', value => {
    return i18n.t(value)
})

Vue.filter('slug', value => {
  return value.toString().substring(0,20).toLowerCase().replace(/\s/g, "-")
})

Vue.filter('twitterhandle', value => {
  if (!value) return ""
  value = value.replace(/\?.*/gi, '')
  return '@'+value.split('/').slice(-1)[0]
})
