<template>
  <v-alert color="grey darken-2" class="ma-4" :value="showAlert">
    <h3 class="mb-2">
      {{ $t('pages.projectManage.evalUpgradeAvailableTitle') }}
    </h3>

    <vue-markdown>{{ $t('pages.projectManage.evalUpgradeAvailable') }}</vue-markdown>

    <v-layout row justify-space-around wrap>
      <v-flex shrink>
        <v-btn dark :to="{name:'help'}" color="blue darken-2">{{ $t('actions.tellMeMore') }}</v-btn>
      </v-flex>
      <v-flex shrink>
        <v-btn dark color="green darken-2" @click="updateProject"><v-icon left>mdi-alert-outline</v-icon> {{ $t('pages.projectManage.evalConvertProject') }}</v-btn>
      </v-flex>
      <v-flex shrink>
        <v-btn dark color="orange darken-4" @click="dissmissAlert">{{ $t('actions.notInterested') }}</v-btn>
      </v-flex>
    </v-layout>
  </v-alert>
</template>

<script>
import Cookies from 'js-cookie'

export default {
  props: ['project'],

  data() {
    return {
      showAlert: false
    }
  },


  mounted() {
    let cookieKey = `eval-dismissed-project-${this.project.id}`;

    let dimissedAlert = Cookies.get(cookieKey)
    this.showAlert = !dimissedAlert && this.project.eval_version == 1
  },

  methods: {
    async updateProject(){
      if(confirm(this.$t('pages.projectManage.evalConfirmUpdate'))){
        try {
          await this.$store.dispatch('project/updateEvaluation', {id:this.project.id, evalVersion:2})
          await this.$store.dispatch("project/load", [this.project.id])
          await this.$store.dispatch("evaluation/loadProject", this.project.id)

          this.$store.dispatch('toast/success', this.$t('pages.projectManage.evalUpgradeSuccess'))
          this.showAlert = false;

        } catch (error) {
          this.$store.dispatch('toast/error', {message: this.$t('pages.projectManage.evalUpgradeError'), error})
        }
      }
    },

    dissmissAlert(){
      this.showAlert = false
      // TODO: rewrite this?
      // if(confirm(this.$t('pages.projectManage.evalConfirmDismiss'))){
      //   let cookieKey = `eval-dismissed-project-${this.project.id}`
      //   Cookies.set(cookieKey, true, { expires: 90,  })
      //   this.showAlert = false
      // }
    }
  },

}
</script>

