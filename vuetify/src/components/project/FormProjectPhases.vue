<template>
  <v-form ref="form" v-model="valid">
    <!-- Title -->
    <v-layout>
      <v-flex grow>
        <h2>{{ $t('pages.projectManage.phasesTab') }}</h2>
      </v-flex>
      <v-flex shrink>
        <v-btn class="elevation-0" fab :outline="!showHelp" :dark="showHelp" small color="blue" @click="showHelp = !showHelp">
          <v-icon>mdi-help</v-icon>
        </v-btn>
      </v-flex>
    </v-layout>

    <!-- Contextual help -->
    <v-alert color="info" class="ma-4" :value="showHelp">
      <v-layout row align-top>
        <v-flex shrink>
          <v-icon large dark>info</v-icon>
        </v-flex>
        <v-flex>
          <vue-markdown>{{ $t('pages.projectManage.phasesTabDescription') }}</vue-markdown>
        </v-flex>
      </v-layout>
    </v-alert>

    <p>{{ $t('pages.evaluationEntry.selfQuestionnaireDescription') }}</p>

    <p class="text-xs-center">
      <v-btn dark color="blue darken-1" href="/learn/?master=12">
        <v-icon left>mdi-file-pdf</v-icon>
        {{ $t('pages.evaluationEntry.viewQuestionnaire1') }}
      </v-btn>
      <br>
      <v-btn dark color="green darken-2" href="/learn/?master=13">
        <v-icon left>mdi-file-pdf</v-icon>
        {{ $t('pages.evaluationEntry.viewQuestionnaire3') }}
      </v-btn>
    </p>

    <h3 v-if="!!currentPhase" class="my-4 headline text-xs-center">
      <!-- <small>{{ $t('pages.projectManage.currentPhase') }}</small> -->
      <b>{{ $t(currentPhase.name) }}</b>
    </h3>

    <h3 v-else class="my-4 headline text-xs-center">
      {{ $t('pages.projectManage.noCurrentPhase') }}
    </h3>

    <h3 class="mb-2">
      {{ $t('pages.projectManage.changePhase') }}
    </h3>

    <v-select v-model="stepperPhase"
              box
              :items="Object.values(phases)"
              item-value="id"
              :item-text="phaseName"
              :label="$t('forms.fields.projectPhase')"
              :rules="[rules.required]"
    />

    <v-card class="my-5">
      <v-stepper
        v-model="stepperPhase"
        class="mb-3 elevation-0"
        alt-labels
      >
        <v-stepper-header class="elevation-0">
          <template v-for="phase in phases">
            <v-stepper-step :key="phase.id" :step="phase.id">
              {{ $t(phase.tag) }}
            </v-stepper-step>
            <v-divider v-if="phase.id != 4" :key="phase.id+'-div'" />
          </template>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content v-for="phase in phases" :key="phase.id" :step="phase.id">
            <h3 class="mb-3">
              {{ $t(phase.name) }}
            </h3>
            <p v-if="getProjectPhase(phase) && getProjectPhase(phase).is_active">
              <i>{{ $t('pages.projectManage.hasPhase', {date: getProjectPhase(phase).date}) }}</i>
            </p>
            <p v-else-if="getProjectPhase(phase)">
              <i>{{ $t('pages.projectManage.hadPhase', {date: getProjectPhase(phase).date}) }}</i>
            </p>
            <p v-else>
              <i>{{ $t('pages.projectManage.notHasPhase') }}</i>
            </p>
            <p>
              {{ $t(phase.name+'Description') }}
            </p>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-card>

    <v-btn block large
           color="success"
           :disabled="!valid || processing"
           :loading="processing"
           @click="attemptSubmit()"
    >
      {{ $t('actions.save') }}
    </v-btn>
  </v-form>
</template>


<script>
import { cloneDeep } from "lodash";
import { ProjectAtPhaseResource } from "@/plugins/resource";

export default {
  props: ["project"],

  data() {
    return {
      showHelp: false,
      valid: null,
      stepperPhase: null,
      processing: false,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
    }
  },

  computed: {
    phases(){
      return this.$store.getters['evaluation/phases']
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

  mounted() {
    this.refreshStepper()
  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
    },

    refreshStepper(){
      this.$nextTick(() =>{
        if (this.currentPhase)
        this.stepperPhase = this.currentPhase.id
      })
    },

    getProjectPhase(phase){
      try{ return this.project.phases.filter(p => p.project_phase == phase.id)[0] }
      catch(err){ return null }
    },

    phaseName(phase){
      return this.$t(phase.name)
    },

    attemptSubmit: async function() {
      if (this.$refs.form.validate()) {

        Object.values(this.phases).forEach(async phase => {
          let projectPhase = this.getProjectPhase(phase)
          let isSelectedPhase = phase.id == this.stepperPhase

          try{
            if(projectPhase){
              // If the project already has the phase, reupdate all
              await ProjectAtPhaseResource.update({id:projectPhase.id},
                {is_active: isSelectedPhase}
              )
            }else if(isSelectedPhase){
              // If the  project does not have it, but is the selected one, create it.
              await ProjectAtPhaseResource.save({
                is_active: true,
                project_phase: phase.id,
                project: this.project.id,
              })
            }
            await this.$store.dispatch("project/load", [this.project.id])
            this.$store.dispatch("toast/success", this.$t('forms.toasts.projectSaveSuccess'))

          }catch(error){
            this.$store.dispatch("toast/error", {
              message: this.$t('forms.toasts.projectSaveFailure'),
              error
            })
          }
        });

        // this.refreshStepper()
      }
    },

  }
}
</script>
