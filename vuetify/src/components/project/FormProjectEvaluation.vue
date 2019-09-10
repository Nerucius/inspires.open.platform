<style scoped>

table{
  width: 100%;
}

</style>


<template>
  <div v-if="project" class="pb-4">
    <h2 class="mb-2">
      {{ $t('pages.projectManage.evaluationTitle') }}
    </h2>

    <v-alert color="info" class="ma-4" :value="true">
      <v-layout row align-top>
        <v-flex>
          <v-icon large dark>
            info
          </v-icon>
        </v-flex>
        <v-flex>
          {{ $t('pages.projectManage.evaluationTabDescription') }}
        </v-flex>
      </v-layout>
    </v-alert>

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
          <v-btn v-if="getProjectPhase(phase) && getProjectPhase(phase).is_active"
                 flat
                 style="flex: 0 0 0"
                 class="my-0"
                 color="success"
          >
            {{ $t("states.current") }}
          </v-btn>
          <v-btn v-else-if="getProjectPhase(phase)"
                 flat
                 style="flex: 0 0 0"
                 class="my-0"
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
                <strong>
                  {{ user(participant.user).full_name }}
                </strong>
              </v-flex>
              <v-flex xs6 sm3>
                {{ $t(roles[participant.role].name) }}
              </v-flex>
              <v-flex xs12 sm6>
                <!-- Send evaluation request -->
                <v-btn
                  v-if="!getEvaluation(phase, participant) && getProjectPhase(phase)"
                  flat
                  block outline class="my-0" @click="sendEvaluationRequest(phase, participant)"
                >
                  {{ $t('pages.projectManage.evalSendRequest') }}
                </v-btn>

                <v-layout wrap>
                  <v-flex lg6 sm12 xs6>
                    <!-- Resend request -->
                    <v-btn v-if="getEvaluation(phase, participant)" block outline
                           color="warning"
                           class="my-0"
                           @click="resendEvaluationRequest(getEvaluation(phase, participant))"
                    >
                      {{ $t('pages.projectManage.evalResendRequest') }}
                    </v-btn>
                  </v-flex>
                  <v-flex lg6 sm12 xs6>
                    <!-- View Evaluation -->
                    <v-btn v-if="getEvaluation(phase, participant)" :outline="!getEvaluation(phase, participant).is_complete" target="_blank" block color="success"
                           class="my-0"
                           :to="{name:'evaluation-entry', params:{ slug: getEvaluation(phase, participant).id}}"
                    >
                      {{ $t('pages.projectManage.evalViewEvaluation') }}
                      <span v-if="getEvaluation(phase, participant).is_complete">
                        &nbsp; {{ $t('pages.projectManage.evalComplete') }}
                      </span>
                    </v-btn>
                  </v-flex>
                </v-layout>
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
        required: v => v!=undefined || this.$t("forms.rules.requiredField"),
      },
    };
  },

  computed: {
    evaluations(){
      return this.$store.getters['evaluation/project'](this.project.id)
    },
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
      return {id:0}
    }
  },

  async mounted() {
    // Load all evaluations for this project
    await this.$store.dispatch("evaluation/loadProject", this.project.id)

    // Opening the phase tab seems to break the overflow
    setTimeout(() => {
      // this.panel[this.currentPhase.id] = [1]
    }, 1000);

  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
    },

    getEvaluation(phase, participant){
      let userEval = this.evaluations
        .filter(e => e.participation == participant.id)
        .filter(e => e.project_phase == phase.id)
      return userEval[0]
    },

    getProjectPhase(phase){
      try{ return this.project.phases.filter(p => p.project_phase == phase.id)[0] }
      catch(err){ return null }
    },

    sendEvaluationRequest: async function(phase, participant) {
      try{
        let response = await this.$store.dispatch("evaluation/create",{
          participation: participant.id,
          phase: this.getProjectPhase(phase).id
        })
        this.$store.dispatch("evaluation/loadProject", this.project.id)
        this.$store.dispatch("toast/success", this.$t('pages.projectManage.evaluationSuccess'))

      }catch(err){
        console.error(error)
        this.$store.dispatch("toast/error", {
          message: this.$t('pages.projectManage.evaluationFailure'),
          error
        })
      }
    },

    resendEvaluationRequest: async function(evaluation) {

      if (!confirm(this.$t('pages.projectManage.evalConfirmResend'))){
        return;
      }

      try{
        let response = await this.$store.dispatch("evaluation/update",{
          id: evaluation.id,
          resend_email: true
        })
        this.$store.dispatch("evaluation/loadProject", this.project.id)
        this.$store.dispatch("toast/success", this.$t('pages.projectManage.evaluationSuccess'))

      }catch(error){
        console.error(error)
        this.$store.dispatch("toast/error", {
          message: this.$t('pages.projectManage.evaluationFailure'),
          error
        })
      }
    },

  }
};
</script>