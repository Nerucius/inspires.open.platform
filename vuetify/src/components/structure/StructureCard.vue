<template>
  <v-card v-if="structure.id">
    <v-img
      style="overflow: visible"
      :src="structure.image_url || defaultImage"
      aspect-ratio="1.75">
    </v-img>

    <v-card-text>
      <v-sheet style="overflow: hidden;" height="150">
        <h2 style="font-size:125%">
          {{ structure.name }}
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
        :to="{name:'structure-detail', params:{slug:obj2slug(structure)}}"
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
      obj2slug,
      defaultImage : "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg"
    }
  },

  methods:{

  }
};
</script>
