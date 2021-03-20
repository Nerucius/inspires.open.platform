<template>
  <v-list three-line="" class="ma-0 pa-0">
    <v-list-tile
      v-for="obj in objects"
      :key="obj.id"
      :to="obj.link"
    >

      <v-list-tile-avatar tile size="60" class="ma-0 pa-0">
        <v-img :src="obj.image_url" :ratio="1" />
      </v-list-tile-avatar>

      <v-list-tile-content class="px-3">
        <v-list-tile-title>{{ obj.name }}</v-list-tile-title>
        <v-list-tile-sub-title>{{ obj.summary }}</v-list-tile-sub-title>
      </v-list-tile-content>

      <v-list-tile-action v-if="showLastModified" style="width:30px !important">
        <v-list-tile-action-text>
          {{ $t('misc.timeAgo', {time: moment(obj.modified_at).fromNow()}) }}
        </v-list-tile-action-text>
        <br>
      </v-list-tile-action>
    </v-list-tile>
  </v-list>
</template>

<script>

export default {

  props: {
    objects:{ required: true },
    showLastModified:{ default: false },
    bigImages: { default: false }
  },

  data() {
    return {
      moment
    }
  },

  methods: {
  }
};
</script>
