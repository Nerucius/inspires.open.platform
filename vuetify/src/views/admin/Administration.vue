<style scoped>
  .container .v-list a{ text-decoration: none; }
  .container .v-list a:hover{ text-decoration: underline; }
</style>


<template>
  <v-layout v-if="authorized" row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.admin.mainTitle') }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-title>
          <h2 class="title">
            OpenPlatform Data Exports
          </h2>
        </v-card-title>
        <v-card-text>
          <vue-markdown>Export all available data from the Platform in CSV format for usage in other tools</vue-markdown>

          <v-list two-line>
            <!-- Project Export -->
            <v-list-tile>
              <v-list-tile-avatar>
                <v-icon>mdi-database-export</v-icon>
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>
                  <strong>
                    All Platform Projects
                  </strong>
                </v-list-tile-title>
                <v-list-tile-sub-title>
                  Download a CSV of all Projects currently in the platform.
                </v-list-tile-sub-title>
              </v-list-tile-content>

              <v-list-tile-action>
                <v-btn color="success" class="elevation-0" @click="exportProjectsCSV()">
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
                  <strong>
                    All Platform Structures
                  </strong>
                </v-list-tile-title>
                <v-list-tile-sub-title>
                  Download a CSV of all Structures currently in the platform.
                </v-list-tile-sub-title>
              </v-list-tile-content>

              <v-list-tile-action>
                <v-btn color="success" class="elevation-0" @click="exportStructuresCSV()">
                  Export
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-title>
          <h2 class="title">
            {{ $t('pages.admin.pendingApproval') }}
          </h2>
        </v-card-title>
        <v-card-text>
          <vue-markdown>{{ $t('pages.admin.instructionsText') }}</vue-markdown>

          <v-list two-line>
            <template v-for="(structure,idx) in structures">
              <v-list-tile :key="structure.id">
                <!-- Structure Image -->
                <v-list-tile-avatar>
                  <!-- <img :src="getUser(structure.created_by).avatar_url"> -->
                  <img :src="structure.image_url">
                </v-list-tile-avatar>

                <!-- Tile content -->
                <v-list-tile-content>
                  <v-list-tile-title>
                    <router-link :to="structure.link">
                      <strong>
                        {{ structure.name }}
                      </strong>
                    </router-link>
                  </v-list-tile-title>
                  <v-list-tile-sub-title>
                    <router-link :to="getUser(structure.created_by).link">
                      {{ $t('pages.admin.createdBy', {name: getUser(structure.created_by).full_name}) }}
                    </router-link>
                  </v-list-tile-sub-title>
                </v-list-tile-content>

                <v-list-tile-action>
                  <v-btn color="success" class="elevation-0" @click="validate(structure.id)">
                    Validate
                  </v-btn>
                </v-list-tile-action>
              </v-list-tile>

              <v-divider v-if="idx != structures.length-1" :key="`div-${structure.id}`" inset />
            </template>
          </v-list>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>

  <!-- Alert for unauthorized -->
  <v-layout v-else>
    <v-flex xs12>
      <v-alert color="error" :value="true" class="headline">
        <v-layout row align-center>
          <v-flex>
            <v-icon large dark>
              warning
            </v-icon>
          </v-flex>
          <v-flex>
            {{ $t('pages.admin.unauthorizedAccess') }}
          </v-flex>
        </v-layout>
      </v-alert>
    </v-flex>
  </v-layout>
</template>

<script>
import { onlyUnique, slug2id, donwloadAsyncCSV} from "@/plugins/utils";
import { cloneDeep } from "lodash";
import { API_SERVER } from "@/plugins/resource";

export default {

  metaInfo(){
    return {
      title: this.$t("pages.admin.mainTitle")
    }
  },


  data(){
    return{
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
    }
  },

  computed:{

    user(){
      return this.$store.getters['user/current']
    },

    authorized(){
      return this.user.is_superuser
    },

    structures(){
      return this.$store.getters['structure/all']
    }

  },


  created(){
    this.loadUnvalidatedStructures()
  },

  methods:{

    async exportProjectsCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/admin/all_projects.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_projects.csv');
    },

    async exportStructuresCSV(){
      let exportUrl = `${API_SERVER}/v1/csv/export/admin/all_structures.csv`;
      await donwloadAsyncCSV(this, exportUrl, 'all_structures.csv');
    },

    getUser(id){
      return this.$store.getters['user/get'](id)
    },

    async loadUnvalidatedStructures(){
      this.$store.dispatch("structure/clear")
      await this.$store.dispatch("structure/load", {
        params:{nonvalidated:true}
      })
    },

    async validate(structureId){

      try{
        await this.$store.dispatch("structure/validate", structureId);
        await this.loadUnvalidatedStructures();
        this.$store.dispatch("toast/success", this.$t("pages.admin.validationSuccess"))

      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.admin.validationFailure"),
          error
        })
      }

    }

  },


};
</script>
