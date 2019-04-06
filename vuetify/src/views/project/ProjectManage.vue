<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.projectManage.title') }}</h1>
    </v-flex>

    <v-flex v-if="isOwner" xs12>
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
        <v-tab v-for="item in page.items" :key="item">
          {{ $t(item) }}
        </v-tab>
      </v-tabs>

      <!-- Tabulation Items -->
      <v-tabs-items v-model="page.tab">
        <!-- Project Detalils Form -->
        <v-tab-item key="page.projectManage.projectTab">
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
        <v-tab-item key="page.projectManage.participantsTab">
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
        <v-tab-item key="page.projectManage.phasesTab">
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

        <v-tab-item key="page.projectManage.evaluationTab">
        </v-tab-item>

      </v-tabs-items>

    </v-flex>

  </v-layout>
</template>

<script>
import FormProjectBase from "@/components/project/FormProjectBase";
import FormProjectParticipants from "@/components/project/FormProjectParticipants";
import FormProjectPhases from "@/components/project/FormProjectPhases";
import FormProjectStructure from "@/components/project/FormProjectStructure";
import { slug2id } from "@/plugins/utils";

export default {
  components: {
    FormProjectBase,
    FormProjectParticipants,
    FormProjectStructure,
    FormProjectPhases,
  },

  data() {
    return {
      dataReady: false,
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
    }
  },

  async mounted() {
    // Important to await before moving on here
    await this.$store.dispatch("project/load", [this.projectId])
    this.dataReady = true
  },

};
</script>
