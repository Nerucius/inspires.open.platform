<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.structureCreate.title') }}</h1>
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

  metaInfo() {
    return {
      title: this.$t('pages.structureCreate.title')
    };
  },

  components:{
    FormStructureBase,
  },

  data(){
    return{
    }
  },

  methods: {

    async createStructure(structureData){
      try{
        let structure = await this.$store.dispatch("structure/create", structureData)

        this.$matomo && this.$matomo.trackEvent('structure', 'structure--create')

        this.$store.dispatch("toast/success", this.$t('pages.structureCreate.success'))
        let slug = obj2slug(structure)
        this.$router.push({name:"structure-manage", params:{slug}})

      } catch(error){
        this.$store.dispatch("toast/error", {
          message:this.$t('pages.structureCreate.failure'),
          error
        })
      }

    }
  }
};
</script>
