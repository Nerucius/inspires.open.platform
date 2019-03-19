<template>
  <v-card v-if="project.id">
    <v-img
      style="overflow: visible"
      :src="project.image_url || defaultImage"
      aspect-ratio="1.75"
    >
      <v-btn
        v-for="(user,idx) in users(project.participants)"
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

    <v-card-text>
      <v-sheet style="overflow: hidden;" height="150">
        <h2 style="font-size:125%">
          {{ project.name }}
        </h2>
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
        :to="{name:'project-detail', params:{slug:obj2slug(project)}}"
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
import { obj2slug } from "@/plugins/utils";

export default {
  props: ['project'],

  data(){
    return{
      obj2slug,
      defaultImage : "https://png.pngtree.com/thumb_back/fw800/back_pic/00/03/14/92561d1ba31f9fe.jpg"
    }
  },

  methods:{
    users(userIds){
      return userIds.map(uid => this.$store.getters["user/get"](uid) )
    },

  }
};
</script>
