import { ParticipationResource } from "../plugins/resource";

export default {
  namespaced: true,

  state: {
  },

  mutations: {

  },

  actions: {
    create: async function (context, object){
      delete object['id']
      let result = await ParticipationResource.save(object)
      let newObject = result.body
      return newObject
    },

    update: async function (context, object){
      let patcheObject = (await ParticipationResource.update({id:object.id}, object))
      return patcheObject
    },

    delete: async function (context, id){
      let result = (await ParticipationResource.delete({id}))
      return result
    },
  },

  getters: {
  }
};