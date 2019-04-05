<style scoped>

  a{
    text-decoration: none;
    color:inherit;
  }

</style>


<template>
  <v-card class="mb-5">
    <v-layout row>
      <v-flex xs4 py-0>
        <v-img height="100%" :src="project.image_url || defaultImage" />
      </v-flex>

      <v-flex xs8 py-2 pr-3>
        <router-link :to="projectLink">
          <h3>{{ project.name }}</h3>
        </router-link>
        <p>{{ project.summary | ellipsis(180) }}</p>

        <div class="text-xs-right">
          <v-btn flat :to="projectLink">
            More
          </v-btn>
        </div>
      </v-flex>
    </v-layout>
  </v-card>
</template>


<script>
import { slug2id, obj2slug } from "@/plugins/utils";

export default {
  props:["project"],


  computed:{
    projectLink(){
      return {name:'project-detail', params:{slug:obj2slug(this.project)}}
    }
  }

}



</script>
