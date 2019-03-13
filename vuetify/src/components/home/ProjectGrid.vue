<template>
  <v-card flat>
    <v-card-text>
      <h1>{{ $t('pages.home.projectsTitle') }}</h1>
      <p />

      <v-container grid-list-xl>
        <v-layout row wrap>
          <v-flex v-for="project in projects" :key="project.id" xs12 sm6 lg4 mb-3>
            <ProjectCard :project="project" />
          </v-flex>
        </v-layout>
      </v-container>

    </v-card-text>
  </v-card>
</template>

<script>
import ProjectCard from "@/components/project/ProjectCard";

export default {

  components:{
    ProjectCard
  },

  props: ["projects"],

  data() {
    return {
      random: Math.random,
      round: Math.round,
      projectSummary:
        "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quidem, vitae facere aperiam expedita esse et iure eos cum laborum eveniet. Praesentium blanditiis similique commodi."
    };
  },

  methods: {
    randomImage() {
      let images = [
        "https://png.pngtree.com/thumb_back/fw800/back_pic/00/01/92/33560de30f1df69.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/03/53/70/335798720153c21.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/00/06/32/355628fc243b919.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/02/65/63/65578876d4f20e9.jpg"
      ];

      let ridx = Math.floor(Math.random() * images.length);
      return images[ridx];
    }
  }
};
</script>
