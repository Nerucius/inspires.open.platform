<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12 sm6>
      <h1>{{ $t('pages.projectManage.title') }}</h1>
      <h2 class="text--grey">
        <small>Project:</small> {{ project.name }}
      </h2>
    </v-flex>

    <v-flex xs12 sm6 class="text-xs-right">
      <v-btn :to="project.link" exact outline>
        {{ $t('actions.viewPublicPage') }}
      </v-btn>
    </v-flex>

    <!-- DISABLED transfer ownership -->
    <v-flex v-if="isOwner && false" xs12>
      <v-card flat>
        <v-card-text>
          <p class="subheading mb-0">
            <strong>
              Project Owner: {{ projectOwner.full_name }}
            </strong>
            <v-btn flat>
              Transfer Ownership
            </v-btn>
          </p>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <!-- Tabulation Menu -->
      <v-tabs v-model="page.tab" grow class="mb-3">
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
        <!-- Project Detalils Form -->
        <v-tab-item key="pages.projectManage.projectTab">
          <v-layout row wrap>
            <v-flex xs12>
              <v-card flat>
                <v-card-text>
                  <FormProjectStructure v-if="dataReady" :project="project" />
                </v-card-text>
              </v-card>
            </v-flex>

            <v-flex xs12>
              <v-card flat>
                <v-card-text>
                  <FormProjectBase v-if="dataReady" :project="project" />
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-tab-item>

        <!-- Project Participants -->
        <v-tab-item key="pages.projectManage.participantsTab">
          <v-layout row wrap>
            <v-flex xs12>
              <v-card flat>
                <v-card-text>
                  <FormProjectParticipants v-if="dataReady" :project="project" />
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-tab-item>

        <!-- Project Phases -->
        <v-tab-item key="pages.projectManage.phasesTab">
          <v-layout row wrap>
            <v-flex xs12>
              <v-card flat>
                <v-card-text>
                  <FormProjectPhases v-if="dataReady" :project="project" />
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-tab-item>

        <v-tab-item key="pages.projectManage.evaluationTab">
          <v-layout row wrap>
            <v-flex xs12>
              <v-card flat style="min-height:85vh">
                <v-card-text>
                  <FormProjectEvaluation v-if="dataReady" :project="project" />
                </v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-tab-item>
      </v-tabs-items>
    </v-flex>
  </v-layout>
</template>

<script>
import FormProjectBase from "@/components/project/FormProjectBase";
import FormProjectParticipants from "@/components/project/FormProjectParticipants";
import FormProjectStructure from "@/components/project/FormProjectStructure";
import FormProjectPhases from "@/components/project/FormProjectPhases";
import FormProjectEvaluation from "@/components/project/FormProjectEvaluation";
import { slug2id } from "@/plugins/utils";

function tabSlug(fullTabName){
  return fullTabName.split('.')[2]
}

export default {
  metaInfo() {
    return {
      title: this.$t('pages.projectManage.title')
    };
  },

  components: {
    FormProjectBase,
    FormProjectParticipants,
    FormProjectStructure,
    FormProjectPhases,
    FormProjectEvaluation,
  },

  data() {
    return {
      dataReady: false,
      activeTab: 1,
      page: {
        tab: null,
        items: [
          "pages.projectManage.projectTab",
          "pages.projectManage.participantsTab",
          "pages.projectManage.phasesTab",
          "pages.projectManage.evaluationTab"
        ]
      },
    }
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    project(){
      return this.$store.getters["project/detail"](this.projectId)
    },
    projectOwner(){
      return this.$store.getters["user/get"](this.project.owner)
    },
    isOwner(){
      return this.projectOwner.id == this.$store.getters['user/current'].id
    },
    activeTabName(){
      return this.page.items[this.page.tab].split('.')[2]
    }
  },

  async mounted() {
    // Important to await before moving on here
    await this.$store.dispatch("project/load", [this.projectId])
    this.dataReady = true

    // Change tab on next tick
    setTimeout(() => {
      this.page.tab = this.getTabForName(this.$route.hash)
    }, 500);

  },

  methods:{
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
