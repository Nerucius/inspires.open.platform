<template>

  <v-list three-line="" class="ma-0 pa-0">

    <v-list-tile
      v-for="project in projects"
      :key="project.id"
      :to="project.link">

      <v-list-tile-avatar tile size="60" class="ma-0 pa-0 mr-3">
        <v-img :src="project.image_url" ratio=1 />
      </v-list-tile-avatar>

      <v-list-tile-content>
        <v-list-tile-title>{{ project.name }}</v-list-tile-title>
        <v-list-tile-sub-title>{{ project.summary }}</v-list-tile-sub-title>
      </v-list-tile-content>

      <v-list-tile-action style="width:30px !important">
        <v-list-tile-action-text >
          {{ $t('misc.timeAgo', {time: moment(project.modified_at).fromNow()}) }}
        </v-list-tile-action-text>
        <br />
      </v-list-tile-action>

    </v-list-tile>

  </v-list>

</template>

<script>

export default {

  props: ["projects"],

  data() {
    return {
      moment
    }
  },

  methods: {
  }
};
</script>
