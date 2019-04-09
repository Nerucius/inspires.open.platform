<style scoped>

table{
  width: 100%;
}

</style>


<template>
  <div v-if="project" class="pb-4">
    <h2 class="mb-2">{{ $t('pages.projectManage.evaluationTitle') }}</h2>

    <p class="subheading mb-5">
      {{ $t('pages.projectManage.evaluationIntro') }}
    </p>

    <v-expansion-panel
      v-for="phase in phases"
      :key="phase.id"
      v-model="panel[phase.id]"
      expand
      class="mb-4"
    >
      <v-expansion-panel-content>
        <!-- Expansion Header with Phase title and Active / Inactive indicator -->
        <template v-slot:header>
          <h3>
            {{ $t(phase.name) }}
          </h3>
          <v-btn
            v-if="getProjectPhase(phase) && getProjectPhase(phase).is_active"
            style="flex: 0 0 0"
            class="my-0" outline
            color="success"
          >
            {{ $t("states.current") }}
          </v-btn>
          <v-btn
            v-else-if="getProjectPhase(phase)"
            style="flex: 0 0 0"
            class="my-0" outline
            color="warning"
          >
            {{ $t("states.inactive") }}
          </v-btn>
        </template>
        <!-- Content of Phase -->
        <v-card>
          <v-card-text>
            <v-layout v-for="participant in project.participants" :key="participant.id" row
                      wrap
                      align-center
                      class="pb-3"
            >
              <v-flex ma-0 xs6 sm3>
                {{ user(participant.user).full_name }}
              </v-flex>
              <v-flex xs6 sm3>
                {{ $t(roles[participant.role].name) }}
              </v-flex>
              <v-flex xs12 sm6>
                <v-btn
                  v-if="!getEvaluation(phase, participant) && getProjectPhase(phase) && getProjectPhase(phase).is_active"
                  flat
                  block outline class="my-0" @click="sendEvaluationRequest(phase, participant)"
                >
                  Send Request for Evaluation
                </v-btn>
              </v-flex>
              <v-flex xs12 py-1>
                <v-divider />
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>


<script>
import { cloneDeep } from "lodash";
import { ProjectAtPhaseResource } from "@/plugins/resource";

export default {
  props: ["project"],

  data() {
    return {
      panel: {1:[0],2:[0],3:[0],4:[0]},
      valid: null,
      processing: false,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
    };
  },

  computed: {
    phases(){
      return this.$store.getters['evaluation/phases']
    },
    roles(){
      return this.$store.getters['evaluation/roles']
    },
    currentPhase(){
      let activePhases = this.project.phases.filter(p => p.is_active)
      if(activePhases.length == 1){
        let phaseId = activePhases[0].project_phase
        return this.phases[phaseId]
      }
      return null
    }
  },

  async mounted() {
    // Load all evaluations for this project
    await this.$store.dispatch("evaluation/loadProject", this.project.id)
    this.$nextTick(() =>{
      this.panel[this.currentPhase.id] = [1]
    })
  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
    },

    getEvaluation(phase, participant){
      let evaluations = this.$store.getters["evaluation/project"](this.project.id)
      let userEval = evaluations
        .filter(e => e.participation == participant.id)
        .filter(e => e.phase == phase.id)
      return userEval[0]
    },

    getProjectPhase(phase){
      try{ return this.project.phases.filter(p => p.project_phase == phase.id)[0] }
      catch(err){ return null }
    },

    sendEvaluationRequest: async function() {
      // TODO: POST new evaluation
      this.$store.dispatch("toast/error", this.$t('pages.projectManage.evaluationFailure'))
    },

  }
};
</script>