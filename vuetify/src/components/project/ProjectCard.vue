<template>
  <v-card v-if="project.id">
    <v-img style="overflow: visible" :src="randomImage()" aspect-ratio="1.75">
      <v-btn
        v-for="(user,idx) in users(project.researchers)"
        :key="user.id"
        icon
        fab
        absolute
        bottom
        right
        class="mb-3"
        :title="`${user.first_name} ${user.last_name}`"
        :style="`margin-right: ${idx*38}px`"
      >
        <v-avatar size="90%">
          <img :alt="user.username" :src="user.avatar_url+'&s=64'">
        </v-avatar>
      </v-btn>
    </v-img>

    <v-card-text style="overflow: hidden;">
      <v-sheet height="150">
        <h3>{{ project.name }}</h3>
        <br>
        <p>{{ project.summary | ellipsis(200) }}</p>
      </v-sheet>
    </v-card-text>
    <v-card-actions>
      <!-- <v-rating
        class="hidden-sm-and-down"
        readonly
        color="orange darken-3"
        background-color="orange darken-3"
        :value="project.rating"
      />
      <v-rating
        class="hidden-md-and-up"
        dense
        readonly
        color="orange darken-3"
        background-color="orange darken-3"
        :value="project.rating"
      />-->
      <v-spacer />
      <v-btn
        flat
        alt="project-see-more"
        :to="{name:'project-detail', params:{slug:slug(project.id, project.name)}}"
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
export default {
  props: ['project'],

  data(){
    return{
      slug
    }
  },

  methods:{
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
    },
  }
};
</script>
