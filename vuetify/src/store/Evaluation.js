import Vue, { ProjectResource } from "../plugins/resource";
import {
  ProjectEvaluationsResource,
  EvaluationResource,
  EvaluationQuestionsResource,
  EvaluationResponsesResource
} from "../plugins/resource";

const Resource = EvaluationResource

function createLink(obj) {
  // obj.link = {
  //   name: "project-detail",
  //   params: {
  //     slug: obj2slug(obj)
  //   }
  // }
  return obj
}

export default {
  namespaced: true,

  state: {
    projects: {},

    itemsDetail: {},

    phases: {
      1: {id:1, name:"models.projectPhase.phase1", tag:"models.projectPhase.phase1Tag"},
      2: {id:2, name:"models.projectPhase.phase2", tag:"models.projectPhase.phase2Tag"},
      3: {id:3, name:"models.projectPhase.phase3", tag:"models.projectPhase.phase3Tag"},
      4: {id:4, name:"models.projectPhase.phase4", tag:"models.projectPhase.phase4Tag"},
    },

    roles: {
      1: {id:1, name:"Scientist", bg:"/img/bg-scientist.png"},
      2: {id:2, name:"Student", bg:"/img/bg-student.png"},
      3: {id:3, name:"Civil Society", bg:"/img/bg-civil.png"},
      4: {id:4, name:"Project Manager", bg:"/img/bg-manager.png"},
    },

    axisNames : {
      "SCIENCE": "models.evaluation.axis.science",
      "COLLECTIVE": "models.evaluation.axis.collective",
      "SCIENCE": "models.evaluation.axis.individial",
    },
    principleNames : {
      "KNOWLEDGE": "models.evaluation.principle.knowledge",
      "CITIZEN": "models.evaluation.principle.citizen",
      "PARTICIPATION": "models.evaluation.principle.participation",
      "TRANSFORM": "models.evaluation.principle.transform",
      "INTEGRITY": "models.evaluation.principle.integrity",
    },
  },

  mutations: {
    SET_PROJECT_EVALS(state, {projectId, items}){
      state.projects = {...state.projects, [projectId]: items}
    },
    ADD_DETAIL(state, items) {
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.id] = i})
      state.itemsDetail = { ...state.itemsDetail, ...newItems }
    },
  },

  actions: {

    load: async function (context, payload={}) {
      if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items = await Promise.all(ids.map(id => Resource.get({id})))
        items = items.map(i => i.body)

        // Get Eval questions
        for (let index = 0; index < items.length; index++) {
          let evaluation = items[index];
          let questions = (await EvaluationQuestionsResource.get({id:evaluation.id})).body
          let responses = (await EvaluationResponsesResource.get({id:evaluation.id})).body
          evaluation.questions = questions.questions
          evaluation.responses = responses.responses
        }

        context.commit("ADD_DETAIL", items)

      }else{
        // No ids provided, just get list of all
        let params = payload.params || {}
        let query = {ordering: "-modified_at", ...params}

        let response = (await Resource.get(query)).body
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

    loadProject: async function(context, projectId){
      let response = (await ProjectEvaluationsResource.get({id:projectId})).body
      let items = response.evaluations

      context.commit("SET_PROJECT_EVALS", {projectId, items})
    },

    create: async function (context, object) {
      let newItem = (await EvaluationResource.save(object)).body
      // await context.dispatch("load", [newItem.id])
      return newItem
    },

    update: async function (context, object) {
      let updatedItem = (await EvaluationResource.update({
        id: object.id
      }, object)).body
      // context.commit("ADD_DETAIL", [updatedItem])
      return updatedItem
    },

    delete: async function (context, id) {
      let result = (await EvaluationResource.delete({
        id
      }))
      // context.dispatch("delete", id)
      return result
    },
  },

  getters: {

    project: state => {
      return (id) => state.projects[id] || []
    },

    detail: state => { return (id) => (state.itemsDetail[id] || {}) },

    phases: state => state.phases,
    roles: state => state.roles,
  }
};