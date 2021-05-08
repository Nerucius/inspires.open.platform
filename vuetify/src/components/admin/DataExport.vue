<template>
  <v-card flat>
    <v-card-title>
      <h2 class="title">OpenPlatform Data Exports</h2>
    </v-card-title>
    <v-card-text>
      <p class="subheading">
        Export all available data from the Platform in CSV format for usage in
        other tools
      </p>

      <v-list two-line>
        <!-- Project Export -->
        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>mdi-database-export</v-icon>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>
              <strong> All Platform Projects </strong>
            </v-list-tile-title>
            <v-list-tile-sub-title>
              Download a CSV of all Projects currently in the platform.
            </v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-btn
              color="success"
              class="elevation-0"
              @click="exportProjectsCSV()"
            >
              Export
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>

        <v-divider />

        <!-- Strucutre Export -->
        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>mdi-database-export</v-icon>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>
              <strong> All Platform Structures </strong>
            </v-list-tile-title>
            <v-list-tile-sub-title>
              Download a CSV of all Structures currently in the platform.
            </v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-btn
              color="success"
              class="elevation-0"
              @click="exportStructuresCSV()"
            >
              Export
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { donwloadAsyncCSV } from "@/plugins/utils";
import { API_SERVER } from "@/plugins/resource";

// TODO: downloadAsyncCSV can be avoided if django returns the correct headers on the CSV request

export default {

  methods: {
    async exportProjectsCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/admin/all_projects.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_projects.csv');
    },

    async exportStructuresCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/admin/all_structures.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_structures.csv');
    },

  },

};
</script>

<style>
</style>
