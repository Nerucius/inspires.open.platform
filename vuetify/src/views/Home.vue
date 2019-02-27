<template>

  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <v-card flat>
        <v-parallax
          height="160"
          src="https://png.pngtree.com/thumb_back/fw800/back_pic/03/51/70/585791ffa147edc.jpg"
        >
          <h1>Welcome to InSPIRES</h1>
        </v-parallax>

        <v-card-text>
          <h1>What we do</h1>
          <br>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo vero quisquam
            quibusdam voluptatibus aut officia corrupti molestias iure ducimus, nemo iste
            dignissimos sint praesentium ab dolorem nesciunt inventore deserunt quam!
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat :to="{name:'about'}">More about us!</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h1>Projects</h1>
          <p></p>

          <v-container grid-list-xl>
            <v-layout row wrap>
              <v-flex xs12 sm6 md4 mb-3 v-for="i in 6" :key="i">
                <v-card>
                  <v-img
                    src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"
                    aspect-ratio="2.00"
                  >
                    <v-avatar v-for="i in round(random()*2)" :key="i"
                      class="ma-2 elevation-3" size="48px">
                      <img src="https://avatars0.githubusercontent.com/u/9064066?v=4&s=460" >
                    </v-avatar>
                  </v-img>

                  <v-card-text style="text-overflow: ellipsis;">
                    <v-sheet height=150>
                      <h3>Project Title</h3>
                      <p></p>
                      <p>
                        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quidem, vitae
                        facere aperiam expedita esse et iure eos cum laborum eveniet. Praesentium
                        blanditiis similique commodi doloremque repellendus placeat, at sint aut.
                      </p>
                    </v-sheet>
                  </v-card-text>
                  <v-card-actions>
                    <v-rating
                      readonly
                      color="orange"
                      background-color="orange"
                      :value="random() * 4 + 2">
                    </v-rating>
                    <v-spacer></v-spacer>
                    <v-btn flat :to="{name:'about'}">
                      More
                      <v-icon right>mdi-chevron-right</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>

          <p class="text-xs-center">
            <v-btn large color="primary">See More Projects</v-btn>
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
              <a href="#">Link one</a><br>
              <a href="#">Link two</a>
            </v-flex>
            <v-spacer></v-spacer>
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
      round: Math.round
    }
  },

  methods: {
    createSubject: function() {
      this.$store.dispatch("subject/add");
    },
    deleteSubject: function(subject) {
      this.$store.dispatch("subject/delete", subject);
    }
  }
};
</script>

