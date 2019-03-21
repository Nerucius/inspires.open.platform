<style scoped>

  .v-chip{
    cursor: pointer;
  }

</style>


<template>
  <v-card v-if="structure.id">
    <v-img
      :src="structure.image_url || defaultImage"
      aspect-ratio="1.75"
    >
      <v-layout fill-height align-end>
        <v-flex xs12 pb-0>
          <v-toolbar style="background-color:rgba(0,0,0,.3)" dense flat>
            <v-chip v-for="area in structure.knowledge_areas.slice(0,3)" :key="area.code"
                    dark color="grey darken-4"
                    :title="area.name"
                    @click="$router.push(`/structures/areas/${obj2slug(area)}`)"
            >
              {{ area.name | ellipsis(16) }}
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


    <v-card-text>
      <v-sheet style="overflow: hidden;" height="150">
        <h2 style="font-size:125%">
          {{ structure.name }} <small>| {{ structure.year_founded }}</small>
        </h2>
        <br>
        <p>{{ structure.summary | ellipsis(200) }}</p>
      </v-sheet>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        flat
        alt="project-see-more"
        :to="link"
      >
        {{ $t('actions.more') }}
        <v-icon right class="hidden-sm-and-down">
          mdi-chevron-right
        </v-icon>
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
      defaultImage : "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg"
    }
  },

  computed:{
    link() {
      return ({name:"structure-detail", params:{slug:obj2slug(this.structure)}})
    }
  },

  methods:{

  }
};
</script>
