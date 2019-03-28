<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>Create new Structure</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <FormStructureBase
            @create="createStructure($event)"
          />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import FormStructureBase from "@/components/structure/FormStructureBase";
import { obj2slug } from "@/plugins/utils";

export default {

  components:{
    FormStructureBase,
  },

  data(){
    return{
    }
  },

  methods: {

    async createStructure(structureData){

      console.log(structureData)
      let message

      try{
        let structure = await this.$store.dispatch("structure/create", structureData)
        message = this.$t('pages.structureCreate.success')
        let slug = obj2slug(structure)
        this.$router.push({name:"structure-manage", params:{slug}})

      } catch(err){
        console.log(err)
        message = this.$t('pages.structureCreate.failure')
      }

    console.log(message)

    }

  }
};
</script>
