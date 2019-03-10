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
      <v-card flat>
        <v-card-text>
          <h1>
            {{ $t('pages.home.projectsTitle') }}
            <small class="subheading">
              | Latest updates
            </small>
          </h1>
          <p />

          <v-container grid-list-xl>
            <v-layout row wrap>
              <v-flex xs12 sm6 lg4 mb-3
                v-for="project in projects"
                :key="project.id"
                >
                <ProjectCard :project="project" />
              </v-flex>
            </v-layout>
          </v-container>

          <p class="text-xs-center">
            <v-btn large dark color="teal darken-2">
              {{ $t('pages.home.projectsSeeMore') }}
            </v-btn>
          </p>
        </v-card-text>
      </v-card>
    </v-flex>


    <v-flex xs12 mt-5>
      <v-card flat>
        <v-card-text>
          <h3>Footer Content</h3>
          <v-layout row>
            <v-flex xs4>
              <a href="#">
                Link one
              </a><br>
              <a href="#">
                Link two
              </a>
            </v-flex>
            <v-spacer />
            <v-flex xs4>
              &copy; Some Company LTD 2019
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import ProjectCard from "@/components/project/ProjectCard";

export default {
  components:{
    ProjectCard,
  },

  data(){
    return{
      slug,
      random: Math.random,
      round: Math.round,
      researchers: {},
    }
  },

  computed:{
    projects(){
      return this.$store.getters["project/all"].slice(0, 6)
    },

  },

  async mounted(){
    await this.$store.dispatch("project/load")
  },

  methods: {

    users(userIds){
      return userIds.map(uid => this.$store.getters["user/get"](uid) )
    },

    randomImage(){
      let images = [
        "https://png.pngtree.com/thumb_back/fw800/back_pic/00/01/92/33560de30f1df69.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/03/53/70/335798720153c21.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/00/06/32/355628fc243b919.jpg",
        "https://png.pngtree.com/thumb_back/fw800/back_pic/02/65/63/65578876d4f20e9.jpg",
      ]
      let ridx = Math.floor(Math.random() * images.length)
      return images[ridx]
    }
  }
};
</script>

