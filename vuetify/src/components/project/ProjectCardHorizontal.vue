<style scoped>
  .v-image{ cursor: pointer; }
  a{
    text-decoration: none;
    color:inherit;
  }
</style>

<template>
  <v-card class="mb-5">
    <v-layout row>
      <v-flex xs4 py-0>
        <v-img
          height="165px"
          :src="project.image_url"
          @click="$router.push(project.link)"
        />
      </v-flex>

      <v-flex xs8 pa-3>
        <router-link :to="project.link">
          <h3 class="text-truncate">
            {{ project.name }}
          </h3>
        </router-link>

        <v-btn v-if="project.knowledge_area" flat class="my-1 mx-0 pa-2 grey lighten-5 caption font-weight-light text-uppercase">
          {{ $t(project.knowledge_area.name) }}
        </v-btn>

        <v-sheet :height="3*21" class="overflow-hidden">
          {{ project.summary | ellipsis(180) }}
        </v-sheet>
      </v-flex>
    </v-layout>
  </v-card>
</template>


<script>
import { slug2id, obj2slug } from "@/plugins/utils";

export default {
  props:["project"],


  computed:{
  }

}



</script>
