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
          <h1>{{ $t('pages.home.projectsTitle') }}</h1>
          <p />

          <v-container grid-list-xl>
            <v-layout row wrap>
              <v-flex v-for="i in 6" :key="i"
                      xs12 sm6 lg4 mb-3
              >
                <v-card>
                  <v-img
                    style="overflow: visible"
                    :src="randomImage()"
                    aspect-ratio="1.75"
                  >
                    <v-btn v-for="(a, idx) in round(random()*2)+1" :key="a" icon fab absolute bottom
                           right class="mb-3"
                           :style="`margin-right: ${idx*38}px`"
                    >
                      <v-avatar size="90%">
                        <img
                          alt="researcher"
                          :src="`https://avatars0.githubusercontent.com/u/${round(random()*100000)}?v=4&s=48`"
                        >
                      </v-avatar>
                    </v-btn>
                  </v-img>

                  <v-card-text style="overflow: hidden;">
                    <v-sheet height="150">
                      <h3>Project Title</h3>
                      <br>
                      <p>
                        {{ projectSummary | ellipsis(220) }}
                      </p>
                    </v-sheet>
                  </v-card-text>
                  <v-card-actions>
                    <v-rating
                      class="hidden-sm-and-down"
                      readonly
                      color="orange darken-3"
                      background-color="orange darken-3"
                      :value="random() * 4 + 2"
                    />
                    <v-rating
                      class="hidden-md-and-up"
                      dense
                      readonly
                      color="orange darken-3"
                      background-color="orange darken-3"
                      :value="random() * 4 + 2"
                    />
                    <v-spacer />
                    <v-btn flat :to="{name:'about'}" alt="project-see-more">
                      {{ $t('actions.more') }}
                      <v-icon right class="hidden-sm-and-down">
                        mdi-chevron-right
                      </v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
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
export default {
  name: "Home",

  data(){
    return{
      random: Math.random,
      round: Math.round,
      projectSummary: "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quidem, vitae facere aperiam expedita esse et iure eos cum laborum eveniet. Praesentium blanditiis similique commodi."
    }
  },

  methods: {
    createSubject: function() {
      this.$store.dispatch("subject/add");
    },

    deleteSubject: function(subject) {
      this.$store.dispatch("subject/delete", subject);
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

