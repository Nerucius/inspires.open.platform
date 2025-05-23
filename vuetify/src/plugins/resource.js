import Vue from "vue"
import VueResource from "vue-resource";

import Cookies from "js-cookie";
Vue.use(VueResource);

export const API_SERVER = process.env.VUE_APP_API_SERVER

// DEPRECATED
// Enable cookie credentials for cross-domain
// Vue.http.options.credentials = true;

// Setup VueResource to work with DRF Token Auth
Vue.http.interceptors.push(function (request) {
  // Normal auth token
  let token = Cookies.get('authorization')
  if (token) {
    request.headers.set('Authorization', `Token ${token}`);
  }

  // Override request headers
  if (!!request.params.headers) {
    console.log("Custom headers set for", request.url)
    for (let key of Object.keys(request.params.headers)) {
      request.headers.set(key, request.params.headers[key])
    }
  }
  // Clean up parameters
  if(request.params.headers !== undefined) { delete request.params['headers']; }
});

// Interceptor to convert aray parameters from
// param[]=1&param[]=2 to:
// param=1&param=2
Vue.http.interceptors.push(function(request, next) {
  if (request.method === "GET") {
    let data = Object.assign({}, request.params);
    for (let i = 0, key; key = Object.keys(data)[i]; i++){
      if (Array.isArray(data[key])){
        request.url+='{?'+key+'*}'
      }
    }
  }
  next();
})

// Add patch method to API resources
const PATCH = {
  patch: {
    method: "PATCH"
  },
  update: {
    method: "PATCH"
  }
}

export const UserResource = Vue.resource(API_SERVER + "/v1/users{/id}/", {}, PATCH);
export const CurrentUserResource = Vue.resource(API_SERVER + "/v1/user/");
export const CUEvaluationsResource = Vue.resource(API_SERVER + "/v1/user/evaluations/");

export const ProjectResource = Vue.resource(API_SERVER + "/v1/projects{/id}/", {}, PATCH);
export const ProjectPhaseResource = Vue.resource(API_SERVER + "/v1/projectphases{/id}/", {}, PATCH);
export const ProjectAtPhaseResource = Vue.resource(API_SERVER + "/v1/projectatphases{/id}/", {}, PATCH);
export const KnowledgeAreaResource = Vue.resource(API_SERVER + "/v1/knowledgeareas{/id}/", {}, PATCH);
export const ParticipationResource = Vue.resource(API_SERVER + "/v1/participations{/id}/", {}, PATCH);
export const StructureResource = Vue.resource(API_SERVER + "/v1/structures{/id}/", {}, PATCH);
export const NetworkResource = Vue.resource(API_SERVER + "/v1/networks{/id}/", {}, PATCH);
export const StructureValidationResource = Vue.resource(API_SERVER + "/v1/structures/validations{/id}/", {}, PATCH);
export const CollaborationResource = Vue.resource(API_SERVER + "/v1/collaborations{/id}/", {}, PATCH);

export const ContentResource = Vue.resource(API_SERVER + "/v1/contents{/id}/", {}, PATCH);
export const FeedbackResource = Vue.resource(API_SERVER + "/v1/feedback{/id}/");

export const ContentTypeResource = Vue.resource(API_SERVER + "/v1/contenttypes/");
export const AttachmentResource = Vue.resource(API_SERVER + "/v1/attachments{/id}/", {}, PATCH);

export const ProjectEvaluationsResource = Vue.resource(API_SERVER + "/v1/eval/project{/id}/", {}, PATCH);
export const ProjectEvaluationStatsResource = Vue.resource(API_SERVER + "/v1/eval/project/stats{/id}/", {}, PATCH);
export const EvaluationResource = Vue.resource(API_SERVER + "/v1/eval/evaluations{/id}/", {}, PATCH);
export const EvaluationQuestionsResource = Vue.resource(API_SERVER + "/v1/eval/questions{/id}/", {}, PATCH);
export const EvaluationResponsesResource = Vue.resource(API_SERVER + "/v1/eval/responses{/id}/", {}, PATCH);
export const QuestionResource = Vue.resource(API_SERVER + "/v1/question{/id}/", {}, PATCH);
export const ResponseResource = Vue.resource(API_SERVER + "/v1/response{/id}/", {}, PATCH);
export const SearchResource = Vue.resource(API_SERVER + "/v1/search?term={term}");

export default Vue
