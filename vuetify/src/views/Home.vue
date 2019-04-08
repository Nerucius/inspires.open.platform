<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <v-card flat>
        <v-parallax
          height="180"
          src="https://png.pngtree.com/thumb_back/fw800/back_pic/03/51/70/585791ffa147edc.jpg"
        >
          <div>
            <h1 class="text-truncate title mb-2">
              {{ $t('pages.home.mainTitle') }}
            </h1>
            <v-sheet :height="3*21" class="transparent white--text overflow-hidden mb-2">
              {{ $t('pages.home.welcomeMessage') }}
            </v-sheet>
            <p class="text-xs-right ma-0">
              <v-btn flat outline dark :to="{name:'about'}">
                {{ $t('pages.home.aboutLink') }}
              </v-btn>
            </p>
          </div>
        </v-parallax>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <ProjectGrid :projects="projects" />

      <p class="text-xs-center mt-3">
        <v-btn large dark color="primary" :to="{name:'project-list'}">
          {{ $t('pages.home.projectsSeeMore') }}
        </v-btn>
      </p>
    </v-flex>
  </v-layout>
</template>

<script>
import ProjectGrid from "@/components/project/ProjectGrid";

export default {
  components: {
    ProjectGrid
  },

  data() {
    return {};
  },

  computed: {
    projects() {
      return this.$store.getters["project/all"];
    }
  },

  mounted(){
    this.$store.dispatch("project/load", {params:{limit:6}})
  }
};
</script>

