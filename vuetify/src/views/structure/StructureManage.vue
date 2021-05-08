<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12 sm6>
      <h1>{{ $t('pages.structureManage.title') }}</h1>
    </v-flex>

    <v-flex xs12 sm6 class="text-xs-right">
      <v-btn :to="structure.link" exact outline>
        {{ $t('actions.viewPublicPage') }}
      </v-btn>
    </v-flex>

    <!-- TODO: Disabled transfer ownership -->
    <v-flex v-if="isOwner && false" xs12>
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
        {{ $t('pages.structureManage.infoNotValidated') }}
      </v-alert>
    </v-flex>


    <v-flex xs12>
      <!-- Tabulation Menu -->
      <v-tabs v-model="page.tab" grow>
        <v-tabs-slider color="primary" />
        <v-tab
          v-for="(item,idx) in page.items" :key="item"
          @click="saveTab(idx)"
        >
          {{ $t(item) }}
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
          <v-card v-if="dataReady" flat>
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
                        <router-link :to="project(collab.project).link">
                          {{ project(collab.project).name }}
                        </router-link>
                      </v-list-tile-title>
                      <v-list-tile-sub-title>
                        {{ project(collab.project).summary }}
                      </v-list-tile-sub-title>
                    </v-list-tile-content>

                    <v-list-tile-action>
                      <v-btn v-if="!collab.is_approved" small
                             color="success"
                             class="elevation-0"
                             @click="approveCollab(collab.id)"
                      >
                        <!-- <v-icon>check</v-icon> -->
                        {{ $t('actions.validate') }}
                      </v-btn>
                      <v-btn v-else small
                             color="error" class="elevation-0"
                             @click="cancelCollab(collab.id)"
                      >
                        <!-- <v-icon>close</v-icon> -->
                        {{ $t('actions.withdraw') }}
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

function tabSlug(fullTabName){
  return fullTabName.split('.')[2]
}

export default {

  metaInfo() {
    return {
      title: this.$t('pages.structureManage.title')
    };
  },

  components: {
    FormStructureBase,
  },

  data() {
    return {
      dataReady: false,
      hasPendingCollabs: false,
      page: {
        tab: null,
        items: [
          "pages.structureManage.structureTab",
          "pages.structureManage.projectsTab"
        ]
      },

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

  async created() {
    // Important to await before moving on here
    await this.$store.dispatch("structure/load", [this.structureId])
    await Promise.all([
      this.$store.dispatch("project/load", this.structure.collaborations.map( c => c.project )),
      this.$store.dispatch("knowledgearea/load"),
      this.$store.dispatch("network/load")
    ])

    let collabs = this.structure.collaborations
    this.hasPendingCollabs = collabs.filter(c => !c.is_approved).length
    if(this.hasPendingCollabs){
      this.$store.dispatch("toast/info", "You have pending requests for collaboration. Please check the projects tab.")
    }
    this.page.tab = this.getTabForName(this.$route.hash)

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
        this.$store.dispatch("toast/success", this.$t("pages.structureManage.collaborationAdded"))

      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.structureManage.collaborationFailure"),
          error
        })
      }
    },

    async cancelCollab(id){
      try{
        await this.$store.dispatch("collaboration/update", {id, is_approved: false})
        await this.$store.dispatch("structure/load", [this.structureId])
        this.$store.dispatch("toast/info", this.$t("pages.structureManage.collaborationRemoved"))

      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.structureManage.collaborationFailure"),
          error
        })
      }
    },

    saveTab(tabIdx){
      this.$router.replace({hash:`${tabSlug(this.page.items[tabIdx])}`})
    },
    getTabForName(tabName){
      return this.page.items
        .map(tabSlug)
        .indexOf(tabName.slice(1))
    }
  }

};
</script>
