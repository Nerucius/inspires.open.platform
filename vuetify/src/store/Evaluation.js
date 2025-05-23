import Vue from "../plugins/resource";
import {
  EvaluationResource,
  QuestionResource,
  ResponseResource,
  ProjectEvaluationsResource,
  EvaluationQuestionsResource,
  EvaluationResponsesResource
} from "../plugins/resource";

const Resource = EvaluationResource

function createLink(obj) {
  return obj
}

export default {
  namespaced: true,

  state: {
    projects: {},

    itemsDetail: {},

    questions: {},

    responses: {},

    phases: {
      1: {id:1, name:"models.projectPhase.phase1", tag:"models.projectPhase.phase1Tag"},
      2: {id:2, name:"models.projectPhase.phase2", tag:"models.projectPhase.phase2Tag"},
      3: {id:3, name:"models.projectPhase.phase3", tag:"models.projectPhase.phase3Tag"},
      4: {id:4, name:"models.projectPhase.phase4", tag:"models.projectPhase.phase4Tag"},
    },

    roles: {
      1: {id:1, name:"models.participationRole.scientist", bg:"/img/bg-scientist.png"},
      2: {id:2, name:"models.participationRole.student", bg:"/img/bg-student.png"},
      3: {id:3, name:"models.participationRole.civilSociety", bg:"/img/bg-civil.png"},
      4: {id:4, name:"models.participationRole.projectManager", bg:"/img/bg-manager.png"},
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
    ADD_RESPONSES(state, items) {
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.id] = i})
      state.responses = { ...state.responses, ...newItems }
    },
    ADD_QUESTIONS(state, items) {
      let newItems = {}
      items.map(createLink).forEach(i => {newItems[i.id] = i})
      state.questions = { ...state.questions, ...newItems }
    },
  },

  actions: {

    load: async function (context, payload) {
      if (!!payload && !!payload.id){
        // Custom callout and arguments
        let item = (await Resource.get({...payload})).body
        let items = [item]

        // Get Eval questions
        for (let index = 0; index < items.length; index++) {
          let evaluation = items[index];
          let questions = (await EvaluationQuestionsResource.get({id:evaluation.id, headers:payload.headers})).body
          let responses = (await EvaluationResponsesResource.get({id:evaluation.id, headers:payload.headers})).body
          evaluation.questions = questions.questions
          evaluation.responses = responses.responses
        }

        context.commit("ADD_DETAIL", items)

      }else if (Array.isArray(payload)){
        // Ids provided, get detailed information on given pids
        let ids = payload
        let items;

        items = await Promise.all(ids.map(id => Resource.get({id})))
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
        let query = payload.params || {}

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

    loadResponses: async function (context, args={}) {
      // Ids provided, get detailed information
      let response = (await ResponseResource.get(args)).body
      context.commit("ADD_RESPONSES", response.results)
    },

    loadQuestions: async function (context, args={}) {
      // Ids provided, get detailed information
      let response = (await QuestionResource.get(args)).body
      context.commit("ADD_QUESTIONS", response.results)
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
      let result = (await EvaluationResource.delete({ id }))
      return result
    },

    submitResponse: async function (context, {response, headers}){
      let result
      if(response.id){
        result = (await ResponseResource.update({id:response.id, headers}, response))
      } else {
        result = (await ResponseResource.save({headers}, response))
      }

      return result
    }
  },

  getters: {

    project: state => {
      return (id) => state.projects[id] || []
    },

    detail: state => { return (id) => (state.itemsDetail[id] || {}) },

    phases: state => state.phases,
    roles: state => state.roles,
    responses: state => Object.values(state.responses),
    questions: state => Object.values(state.questions)
  }
};
