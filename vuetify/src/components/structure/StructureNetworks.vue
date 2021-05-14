<template>
  <v-flex v-if="networks.length > 0">
    <h2>{{ $t('components.StructureNetworks.title') }}</h2>

    <div v-for="network in networks" :key="network.id" class="mt-4">
      <v-expansion-panel>
        <v-expansion-panel-content>
          <template v-slot:header>
            <h3 class="">{{ network.name }}</h3>
          </template>

          <!-- <h4 class="mb-3 ml-4">{{ $t('components.StructureNetworks.otherStructures') }}</h4> -->

          <div class="hidden-sm-and-down px-3 pb-3">
            <div style="overflow-x: auto; white-space: nowrap;">
              <div v-for="structure in network.structures.filter(s => s.id != skip)"
                   :key="structure.id"
                   class="mr-4 mb-4"
                   style="display: inline-block; width: 268px; white-space:initial"
              >
                <StructureCard :structure="structure" :summary="false" />
              </div>
            </div>
          </div>
          
          <div class="hidden-md-and-up">
            <v-card>
              <v-sheet style="max-height: 235px; overflow-y:auto">
                <ModelList :show-last-modified="false" :objects="network.structures.filter(s => s.id != skip)" />
              </v-sheet>
            </v-card>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </div>
  </v-flex>
</template>

<script>
import StructureCard from "@/components/structure/StructureCard";
import ModelList from "@/components/generic/ModelList";


export default {
  components: {
    StructureCard,
    ModelList,
  },
  
  props: ['networks','skip'],

  async created(){
    // let allStructures = this.networks.map(n => n.structures).reduce( (a,b) => a.concat(b) );
    // console.log(allStructures);
    // this.$store.dispatch('structure/load', allStructures);
  }
}
</script>

<style>

</style>
