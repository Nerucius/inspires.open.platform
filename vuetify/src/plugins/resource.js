import Vue from "vue"
import VueResource from "vue-resource";

import Cookies from "js-cookie";
Vue.use(VueResource);

export const API_SERVER = process.env.VUE_APP_API_SERVER

// DEPRECATED
// Enable cookie credentials for cross-domain
// Vue.http.options.credentials = true;

// Setup VueResource to work with DRF Token Auth
Vue.http.interceptors.push(function(request) {
  let token = Cookies.get('authorization')
  if(token){
    console.log("Used auth token")
    request.headers.set('Authorization', `Token ${token}`);
  }
});

// Add patch method to API resources
const PATCH =  {patch: {method: "PATCH"}, update: {method: "PATCH"}}

export const CurrentUserResource = Vue.resource(API_SERVER + "/v1/user/");
export const UserResource = Vue.resource(API_SERVER + "/v1/users/", {}, PATCH);
export const ProjectResource = Vue.resource(API_SERVER + "/v1/projects{/id}/", {}, PATCH);
export const KnowledgeAreaResource = Vue.resource(API_SERVER + "/v1/knowledgeareas{/id}/", {}, PATCH);
export const ParticipationResource = Vue.resource(API_SERVER + "/v1/participations{/id}/", {}, PATCH);
export const StructureResource = Vue.resource(API_SERVER + "/v1/structures{/id}/", {}, PATCH);
export const CollaborationResource = Vue.resource(API_SERVER + "/v1/collaborations{/id}/", {}, PATCH);

export default Vue
