<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.structureManage.title') }}</h1>
    </v-flex>

    <v-flex v-if="isOwner" xs12>
      <v-card flat>
        <v-card-text>
          <p class="subheading mb-0">
            <strong>
              Structure Owner: {{ structureOwner.full_name }}
            </strong>
            <v-btn flat>
              Transfer Ownership
            </v-btn>
          </p>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <FormStructureBase v-if="dataReady" :structure="structure" />
        </v-card-text>
      </v-card>
    </v-flex>

  </v-layout>
</template>

<script>
import FormStructureBase from "@/components/structure/FormStructureBase";
import { slug2id } from "@/plugins/utils";
// import toastr from 'toastr'

export default {
  components: {
    FormStructureBase,
    // FormStructureParticipants,
    // FormStructureStructure,
  },

  data() {
    return {
      dataReady: false,
    }
  },

  computed: {
    structureId() {
      return slug2id(this.$route.params.slug);
    },
    structure(){
      return this.$store.getters["structure/detail"](this.structureId)
    },
    structureOwner(){
      return this.$store.getters["user/get"](this.structure.owner)
    },
    isOwner(){
      return this.structureOwner.id == this.$store.getters['user/current'].id
    }
  },

  async mounted() {
    // Important to await before moving on here
    await this.$store.dispatch("structure/load", [this.structureId])
    await this.$store.dispatch("knowledgearea/load")
    this.dataReady = true
  },

};
</script>
