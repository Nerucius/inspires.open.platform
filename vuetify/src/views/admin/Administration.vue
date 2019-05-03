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
          <h1 class="title">
            {{ $t('pages.admin.pendingApproval') }}
          </h1>
        </v-card-title>
        <v-card-text>

          <vue-markdown>{{ $t('pages.admin.instructionsText') }}</vue-markdown>

          <v-list two-line>

            <template v-for="(structure,idx) in structures">

              <v-list-tile  :key="structure.id">

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
                  <v-btn @click="validate(structure.id)" color="success" class="elevation-0">Validate</v-btn>
                </v-list-tile-action>

              </v-list-tile>

              <v-divider inset v-if="idx != structures.length-1" :key="`div-${structure.id}`"></v-divider>

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
import { onlyUnique, slug2id } from "@/plugins/utils";
import { cloneDeep } from "lodash";
import VueMarkdown from 'vue-markdown';

export default {

  metaInfo(){
    return {
      title: this.$t("pages.admin.mainTitle")
    }
  },

  components:{
    VueMarkdown
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


  created(){
    this.loadUnvalidatedStructures()
  },

  methods:{

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
        console.log(error)
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.admin.validationFailure"),
          error
        })
      }

    }

  },

  computed:{

    user(){
      return this.$store.getters['user/current']
    },

    authorized(){
      return this.user.is_administrator
    },

    structures(){
      return this.$store.getters['structure/all']
    }

  },


};
</script>
