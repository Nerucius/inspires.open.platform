<template>
  <v-layout row wrap align-content-start>

    <v-flex xs12>
      <h1 class="mb-3">
        {{ $t('noums.structures') }}
      </h1>

      <v-expansion-panel>
        <v-expansion-panel-content>
          <template v-slot:header>
            <div class="subheading">Want to know more about structures?</div>
          </template>
          <v-card class="px-3 py-2">
            <vue-markdown>{{ $t('pages.structureList.introText') }}</vue-markdown>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>

    </v-flex>

    <v-flex xs12>

      <v-layout row wrap>
        <v-flex v-for="structure in structures" :key="structure.id" xs12 sm6 md4 lg3 xl2 mb-3>
          <StructureCard :structure="structure" />
        </v-flex>
      </v-layout>

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
    this.$store.dispatch("structure/clear")
    this.$store.dispatch("structure/load")
  }
};
</script>

