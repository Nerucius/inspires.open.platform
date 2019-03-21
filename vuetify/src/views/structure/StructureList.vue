<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h1>{{ $t('pages.structures.title') }}</h1>
          <p />

          <v-container grid-list-xl>
            <v-layout row wrap>
              <v-flex v-for="structure in structures" :key="structure.id" xs12 sm6 lg4 mb-3>
                <StructureCard :structure="structure" />
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>


<script>
import StructureCard from "@/components/structure/StructureCard";

export default {

  metaInfo:{
    title: "All Structures"
  },

  components: {
    StructureCard
  },

  data() {
    return {};
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"];
    }
  },

  mounted(){
    this.$store.dispatch("structure/load")
  }
};
</script>

