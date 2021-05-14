<template>
  <v-list v-if="!!attachments && attachments.length > 0">
    <transition-group name="list">
      <v-list-tile v-for="att in attachments" :key="att.id">
        <v-list-tile-avatar>
          <v-icon>mdi-file</v-icon>
        </v-list-tile-avatar>
        <v-list-tile-content>
          {{ att.name }}
          <small class="grey--text">
            {{ att.mime_type }}, {{ sizeToStr(att.size) }}
          </small>
        </v-list-tile-content>
        <v-list-tile-action style="flex-direction: unset">
          <v-btn
            icon
            ripple
            :href="att.url"
            :download="att.name"
            target="_blank"
          >
            <v-icon color="primary">download</v-icon>
          </v-btn>
          <template v-if="currentUser.is_editor">
            <v-btn
              icon
              ripple
              class="ml-1"
              :href="editAttachmentLink(att)"
              target="_blank"
            >
              <v-icon color="orange">edit</v-icon>
            </v-btn>
            <v-btn icon ripple class="ml-1" @click="deleteAttachment(att)">
              <v-icon color="red">delete</v-icon>
            </v-btn>
          </template>
        </v-list-tile-action>
      </v-list-tile>
    </transition-group>
  </v-list>
  <v-card v-else flat>
    <v-card-text>
      {{ $t('components.Attachment.noAttachments') }}
    </v-card-text>
  </v-card>
</template>


<script>
import { API_SERVER } from "@/plugins/resource";

export default {
  props: ["attachments"],

  computed: {
    currentUser(){
      return this.$store.getters['user/current']
    },
  },

  methods: {
    editAttachmentLink(att) {
      return `${API_SERVER}/admin/backend/attachment/${att.id}/change/`;
    },
    async deleteAttachment(att) {
      if (confirm("Are you sure you want to delete this attachment?")) {
        await this.$store.dispatch("attachment/delete", att.id);
        this.$emit('change')
      }
    },
    sizeToStr(size) {
      let number = size / 1024;
      let unit = "KB";
      if (size / 1024 > 1024) {
        number = size / (1024 * 1024);
        unit = "MB";
      }

      return Math.round(number * 100) / 100 + " " + unit;
    },
  },
};
</script>
