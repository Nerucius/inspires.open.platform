<template>
  <div>
    <h2 class="mb-2">
      {{ $t('pages.projectManage.attachmentsTab') }}
    </h2>

    <v-alert color="info" class="ma-4" :value="true" dismissible>
      <v-layout row align-top>
        <v-flex>
          <v-icon large dark>
            info
          </v-icon>
        </v-flex>
        <v-flex>
          {{ $t('pages.projectManage.attachmentsTabDescription') }}
        </v-flex>
      </v-layout>
    </v-alert>

    <h3>Uploaded Attachments</h3>

    <v-card class="my-4 pa-0">
      <v-list two-line>
        <template v-for="(att,idx) in attachments">
          <v-list-tile :key="att.id">
            <!-- Structure Image -->
            <v-list-tile-avatar>
              <!-- <img :src="getUser(structure.created_by).avatar_url"> -->
              <!-- <img :src="structure.image_url"> -->
              <v-icon>mdi-file</v-icon>
            </v-list-tile-avatar>

            <!-- Tile content -->
            <v-list-tile-content>
              <v-list-tile-title>
                <strong>
                  {{ att.name }}
                </strong>
              </v-list-tile-title>
              <v-list-tile-sub-title>
                MIME Type : {{ att.mime_type }}
                &nbsp; | &nbsp;
                Uploaded on: {{ att.created_at.format('LLL') }}
              </v-list-tile-sub-title>
            </v-list-tile-content>

            <v-btn color="success" class="elevation-0">
              Download
            </v-btn>
            <v-btn color="error" class="elevation-0">
              Delete
            </v-btn>
          </v-list-tile>

          <v-divider v-if="idx != attachments.length-1" :key="`div-${att.id}`" inset />
        </template>
      </v-list>
    </v-card>
  </div>
</template>

<script>
export default {
  props: ["project"],
  data() {
    return {};
  },

  computed: {
    attachments(){
      return [
        {
          id: 1,
          url: "https://example.org",
          name: "Example Image File",
          mime_type: "image/png",
          created_at: moment()
        },
        {
          id: 2,
          url: "https://example.org",
          name: "Example Video File",
          mime_type: "video/webm",
          created_at: moment()
        },
      ]
    }
  },

  created() {

  },

  methods: {

  },
};
</script>
