import Vue, { ProjectResource } from "../plugins/resource";
import {
  ProjectEvaluationsResource,
  EvaluationResource,
  EvaluationQuestionsResource,
  EvaluationResponsesResource
} from "../plugins/resource";


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
      1: {id:1, name:"Scientist"},
      2: {id:2, name:"Student"},
      3: {id:3, name:"Civil Society"},
      4: {id:4, name:"Project Manager"},
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
    }
  },

  actions: {
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


    phases: state => state.phases,
    roles: state => state.roles,
  }
};