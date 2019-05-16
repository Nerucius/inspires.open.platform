<style scoped>
  .v-image{ cursor: pointer; }
  .v-chip{ cursor: pointer; }
  h2 > a{
    text-decoration: none;
    color:inherit;
  }
</style>


<template>
  <v-card v-if="structure.id">
    <v-img
      :src="structure.image_url"
      height="180"
      @click="$router.push(structure.link)"
    >
      <v-layout fill-height align-end>
        <v-flex xs12 pb-0>
          <v-toolbar style="background-color:rgba(0,0,0,.3)" dense flat>
            <v-chip v-for="area in structure.knowledge_areas.slice(0,3)" :key="area.code"
                    dark color="grey darken-4"
                    :title="$t(area.name)"
                    @click="$router.push(`/structures/areas/${obj2slug(area)}`)"
            >
              {{ $t(area.name) }}
            </v-chip>
            <v-chip v-if="structure.knowledge_areas.length > 3" dark
                    color="grey darken-4"
            >
              ...
            </v-chip>
          </v-toolbar>
        </v-flex>
      </v-layout>
    </v-img>


    <v-card-text class="pb-0">
      <h2 style="font-size:125%" class="mb-2">
        <router-link :to="structure.link">
          {{ structure.name }} <small>| {{ structure.year_founded }}</small>
        </router-link>
      </h2>
      <v-sheet :height="4*21" class="overflow-hidden mb-2">
        {{ structure.summary | ellipsis(200) }}
      </v-sheet>
    </v-card-text>
    <v-card-actions>
      <v-btn flat block :to="structure.link">
        {{ $t('pages.structureList.visitStructure') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>


<script>
import { obj2slug } from "@/plugins/utils";

export default {
  props: ['structure'],

  data(){
    return{
    }
  },

  methods:{

  }
};
</script>
