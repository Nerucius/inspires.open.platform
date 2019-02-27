<template>
  <v-layout>

    <v-flex xs12>
      <v-card>
        <v-toolbar card dense dark color="info">
          <v-icon>info</v-icon>
          <v-toolbar-title>About page</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo vero quisquam
            quibusdam voluptatibus aut officia corrupti molestias iure ducimus, nemo iste
            dignissimos sint praesentium ab dolorem nesciunt inventore deserunt quam!
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo vero quisquam
            quibusdam voluptatibus aut officia corrupti molestias iure ducimus, nemo iste
            dignissimos sint praesentium ab dolorem nesciunt inventore deserunt quam!
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat>Create!</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>

  </v-layout>
</template>

<script>
export default {
  name: "About",
  data() {
    return {};
  },
  components: {}
};
</script>
