<template>
  <v-form ref="form" v-model="valid">
    <h2 class="mb-2">{{ $t('pages.projectManage.phasesTab') }}</h2>

    <p class="subheading">
      {{ $t('pages.projectManage.phasesTabDescription') }}
    </p>

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
            <p v-if="getPhase(phase) && getPhase(phase).is_active">
              <i>{{ $t('pages.projectManage.hasPhase', {date: getPhase(phase).date}) }}</i>
            </p>
            <p v-else-if="getPhase(phase)">
              <i>{{ $t('pages.projectManage.hadPhase', {date: getPhase(phase).date}) }}</i>
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

    <h3 class="mb-2">
      Change the current Phase
    </h3>

    <v-select v-model="stepperPhase"
              box
              item-value="id"
              item-text="display"
              :items="phases"
              :label="$t('forms.fields.projectPhase')"
              :rules="[rules.required]"
    />

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
      valid: null,
      stepperPhase: null,
      processing: false,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
      phases: [
        {id:1, name:"models.projectPhase.phase1", display:this.$t("models.projectPhase.phase1"), tag:"models.projectPhase.phase1Tag"},
        {id:2, name:"models.projectPhase.phase2", display:this.$t("models.projectPhase.phase2"), tag:"models.projectPhase.phase2Tag"},
        {id:3, name:"models.projectPhase.phase3", display:this.$t("models.projectPhase.phase3"), tag:"models.projectPhase.phase3Tag"},
        {id:4, name:"models.projectPhase.phase4", display:this.$t("models.projectPhase.phase4"), tag:"models.projectPhase.phase4Tag"},
      ],
    };
  },

  computed: {
    currentPhase(){
      let phaseId
      try{
        phaseId = this.project.phases.filter(p => p.is_active)[0].id
      }
      catch(err){
        phaseId = 1
      }
      return this.phases.filter(p => p.id == phaseId)[0]
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
        this.stepperPhase = this.currentPhase.id
      })
    },

    getPhase(phase){
      try{ return this.project.phases.filter(p => p.id == phase.id)[0] }
      catch(err){ return null }
    },

    attemptSubmit: async function() {
      if (this.$refs.form.validate()) {

        this.phases.forEach(async phase => {
          let projectPhase = this.getPhase(phase)
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

          }catch(err){
            this.$store.dispatch("toast/error", this.$t('forms.toasts.projectSaveFailure'))
          }
        });

        // this.refreshStepper()
      }
    },

  }
};
</script>