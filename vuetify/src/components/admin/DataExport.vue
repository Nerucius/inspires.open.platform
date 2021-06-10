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
              Download a file of all Projects currently in the platform.
            </v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action style="flex-direction: row; align-items:center">
            <v-btn icon ripple
                   :href="exportProjectsCsvURL"
                   title="Download as CSV file"
            >
              <v-icon color="primary">mdi-format-columns</v-icon>
            </v-btn> &nbsp; &nbsp;
            <v-btn icon ripple
                   title="Download as Excel file"
                   :href="exportProjectsExcelURL"
            >
              <v-icon color="primary">mdi-file-excel</v-icon>
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
              Download a file of all Structures currently in the platform.
            </v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action style="flex-direction: row; align-items:center">
            <v-btn
              icon
              ripple
              :href="exportStructuresCsvURL"
              title="Download as CSV file"
            >
              <v-icon color="primary">mdi-format-columns</v-icon>
            </v-btn> &nbsp; &nbsp;
            <v-btn
              icon
              ripple
              title="Download as Excel file"
              :href="exportStructuresExcelURL"
            >
              <v-icon color="primary">mdi-file-excel</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>

        <v-divider />

        <!-- Evaluation Export -->
        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>mdi-database-export</v-icon>
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>
              <strong> All Evaluations from All Projects </strong>
            </v-list-tile-title>
            <v-list-tile-sub-title>
              Download a file of all Evaluations currently in the platform.
            </v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action style="flex-direction: row; align-items:center">
            <v-btn
              icon
              ripple
              title="Download as Excel file"
              :href="exportEvaluationsExcelURL"
            >
              <v-icon color="primary">mdi-file-excel</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import Cookies from 'js-cookie'
import { donwloadAsyncCSV } from "@/plugins/utils";
import { API_SERVER } from "@/plugins/resource";
// TODO: downloadAsyncCSV can be avoided if django returns the correct headers on the CSV request

const AUTH_TOKEN = Cookies.get("authorization")

export default {

  computed:{
    exportProjectsCsvURL(){
      return `${API_SERVER}/v1/csv/export/admin/projects/csv?token=${AUTH_TOKEN}`;
    },
    exportProjectsExcelURL(){
      return `${API_SERVER}/v1/csv/export/admin/projects/xlsx?token=${AUTH_TOKEN}`;
    },
    exportStructuresCsvURL(){
      return `${API_SERVER}/v1/csv/export/admin/structures/csv?token=${AUTH_TOKEN}`;
    },
    exportStructuresExcelURL(){
      return `${API_SERVER}/v1/csv/export/admin/structures/xlsx?token=${AUTH_TOKEN}`;
    },
    exportEvaluationsExcelURL(){
      return `${API_SERVER}/v1/csv/export/admin/evaluations/xlsx?token=${AUTH_TOKEN}`;
    },
  },


  methods: {
    // deprecated
    async exportProjectsCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/admin/all_projects.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_projects.csv');
    },
    // deprecated
    async exportStructuresCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/admin/all_structures.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_structures.csv');
    },

  },

};
</script>

<style>
</style>
