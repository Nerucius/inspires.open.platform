import Vue from "vue"
import VueResource from "vue-resource";

import Cookies from "js-cookie";
Vue.use(VueResource);

// Enable cookie credentials for cross-domain
Vue.http.options.credentials = true;

export const API_SERVER = process.env.VUE_APP_API_SERVER

// Setup VueResource to work with Django CSRF token

export const refreshCSRFCookie = async function () {
  let response = await Vue.http.get(API_SERVER + '/csrf_token/')
  let csrfToken = response.data.csrf_token
  Cookies.set("csrftoken", csrfToken);
  Vue.http.headers.common['X-CSRFToken'] = csrfToken

  console.log("refreshCSRFCookie: ", csrfToken)
}

refreshCSRFCookie();

// Add patch method to API resources
const PATCH =  {patch: {method: "PATCH"}, update: {method: "PATCH"}}

export const CurrentUserResource = Vue.resource(API_SERVER + "/v1/user/");
export const UserResource = Vue.resource(API_SERVER + "/v1/users/", {}, PATCH);
export const ProjectResource = Vue.resource(API_SERVER + "/v1/projects{/id}/", {}, PATCH);
export const StructureResource = Vue.resource(API_SERVER + "/v1/structures{/id}/", {}, PATCH);
export const CollaborationResource = Vue.resource(API_SERVER + "/v1/collaborations{/id}/", {}, PATCH);

export default Vue
