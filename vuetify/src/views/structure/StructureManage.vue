<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12 sm6>
      <h1>{{ $t('pages.structureManage.title') }}</h1>
    </v-flex>
    <v-flex xs12 sm6 class="text-xs-right">
      <v-btn :to="structureLink" outline color="success">
        View public page
      </v-btn>
    </v-flex>

    <v-flex v-if="isOwner" xs12>
      <v-card flat>
        <v-card-text>
          <p class="subheading mb-0">
            <strong>
              Structure Owner: {{ structureOwner.full_name }}
            </strong>
            <v-btn flat>
              Transfer Ownership
            </v-btn>
          </p>
        </v-card-text>
      </v-card>
    </v-flex>

    <!-- Validation Alert -->
    <v-flex v-if="!structure.validation" xs12>
      <v-alert color="info" :value="true" class="subheading">
        <v-icon dark>
          info
        </v-icon>
        This structure has not been validated yet and so will not show up in public lists.
        Please wait until a platform agent activates this structure..
      </v-alert>
    </v-flex>


    <v-flex xs12>
      <!-- Tabulation Menu -->
      <v-tabs
        v-model="page.tab"
        grow
      >
        <v-tabs-slider color="primary" />
        <v-tab v-for="item in page.items" :key="item">
          {{ item }}
        </v-tab>
      </v-tabs>

      <!-- Tabulation Items -->
      <v-tabs-items v-model="page.tab">
        <!-- Structure Form -->
        <v-tab-item key="This Structure">
          <v-card flat>
            <v-card-text>
              <FormStructureBase v-if="dataReady" :structure="structure" />
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- Project Collaboration Forms -->
        <v-tab-item key="Projects">
          <v-card flat>
            <v-card-text>
              <v-list two-line>
                <template v-for="collab in structure.collaborations">
                  <v-list-tile
                    :key="collab.id"
                    :style="{'border-left': collab.is_approved ? '' : '4px solid red'}"
                  >
                    <v-list-tile-avatar>
                      <img :src="user(project(collab.project).owner).avatar_url">
                    </v-list-tile-avatar>

                    <v-list-tile-content>
                      <v-list-tile-title>
                        {{ project(collab.project).name }}
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{ project(collab.project).summary }}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>

                    <v-list-tile-action>
                      <v-btn v-if="!collab.is_approved" small fab
                             color="success"
                             class="elevation-0"
                             @click="approveCollab(collab.id)"
                      >
                        <v-icon>check</v-icon>
                      </v-btn>
                      <v-btn v-else small fab
                             color="error" class="elevation-0"
                             @click="cancelCollab(collab.id)"
                      >
                        <v-icon>close</v-icon>
                      </v-btn>
                    </v-list-tile-action>
                  </v-list-tile>
                  <v-divider :key="collab.id+'-d2'" />
                </template>
              </v-list>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-flex>
  </v-layout>
</template>

<script>
import FormStructureBase from "@/components/structure/FormStructureBase";
import { slug2id, obj2slug } from "@/plugins/utils";

export default {
  components: {
    FormStructureBase,
    // FormStructureParticipants,
    // FormStructureStructure,
  },

  data() {
    return {
      page: {
        tab: null,
        items: [
          "This Structure",
          "Projects"
        ]
      },
      dataReady: false,
      hasPendingCollabs: false,
    }
  },

  computed: {
    structureId() {
      return slug2id(this.$route.params.slug);
    },
    structure(){
      return this.$store.getters["structure/detail"](this.structureId)
    },
    structureOwner(){
      return this.$store.getters["user/get"](this.structure.owner)
    },
    isOwner(){
      return this.structureOwner.id == this.$store.getters['user/current'].id
    },
    structureLink(){
      return ({name:"structure-detail", params:{slug:obj2slug(this.structure)}})
    }
  },

  async mounted() {
    // Important to await before moving on here
    await this.$store.dispatch("structure/load", [this.structureId])
    await this.$store.dispatch("project/load", this.structure.collaborations.map( c => c.project ))
    await this.$store.dispatch("knowledgearea/load")

    let collabs = this.structure.collaborations
    this.hasPendingCollabs = collabs.filter(c => !c.is_approved).length
    if(this.hasPendingCollabs){
      this.$store.dispatch("toast/info", "You have pending requests for collaboration. Please check the projects tab.")
    }

    this.dataReady = true
  },

  methods:{
    user(id){
      return this.$store.getters["user/get"](id)
    },
    project(id){
      return this.$store.getters["project/detail"](id)
    },
    async approveCollab(id){
      try{
        await this.$store.dispatch("collaboration/update", {id, is_approved: true})
        await this.$store.dispatch("structure/load", [this.structureId])
        this.$store.dispatch("toast/success", "Project has been approved under this structure.")

      }catch(err){
        console.error(err)
        this.$store.dispatch("toast/error", "Something has gone wrong, please try again later.")
      }

    },
    async cancelCollab(id){
      try{
        await this.$store.dispatch("collaboration/update", {id, is_approved: false})
        await this.$store.dispatch("structure/load", [this.structureId])
        this.$store.dispatch("toast/info", "Project has been removed from this structure.")

      }catch(err){
        console.error(err)
        this.$store.dispatch("toast/error", "Something has gone wrong, please try again later.")
      }
    },
  }

};
</script>
