<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <v-card flat>
        <v-parallax
          height="180"
          src="https://png.pngtree.com/thumb_back/fw800/back_pic/03/51/70/585791ffa147edc.jpg"
        >
          <h1>{{ $t('pages.home.mainTitle') }}</h1>
        </v-parallax>

        <v-card-text>
          <h1>{{ $t('pages.home.aboutTitle') }}</h1>
          <br>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo vero quisquam
          quibusdam voluptatibus aut officia corrupti molestias iure ducimus, nemo iste
          dignissimos sint praesentium ab dolorem nesciunt inventore deserunt quam!
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn flat :to="{name:'about'}">
            {{ $t('pages.home.aboutLink') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <ProjectGrid />
    </v-flex>

  </v-layout>
</template>

<script>
import ProjectGrid from "@/components/home/ProjectGrid";

export default {

components:{
    ProjectGrid
  },

  data(){
    return{
      slug,
      random: Math.random,
      round: Math.round,
    }
  },

  methods: {


  }
};
</script>

