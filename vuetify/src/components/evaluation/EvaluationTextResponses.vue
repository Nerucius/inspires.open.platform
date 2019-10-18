<template>
  <v-card v-if="textResponses.length > 0">
    <v-card-title>
      <h2 class="title">
        {{ $t('pages.evaluationDetail.commentsByParticipants') }}
      </h2>
    </v-card-title>
    <v-card-text>
      <v-sheet :max-height="200" style="overflow-y:auto; overflow-x:hidden">
        <v-layout ma-0 pa-0 wrap>
          <!-- Single participant quote -->
          <v-flex v-for="response in textResponses" :key="response.id" class="quote" xs12 md6 xl4>
            <vue-markdown>{{ response.answer_text }}</vue-markdown>
          </v-flex>
        </v-layout>
      </v-sheet>
    </v-card-text>
  </v-card>
</template>

<script>
export default {

  props: ["projectId"],

  computed: {
      textResponses(){
      return this.$store.getters['evaluation/responses'].filter(r => r.question.length == 5)
    },
  },

  async created() {
    // Load evaluations
    try{
      await this.$store.dispatch("evaluation/loadProject", this.projectId)
      var evalIds = this.$store.getters['evaluation/project'](this.projectId).map(ev => ev.id)
      this.$store.dispatch("evaluation/loadResponses", evalIds)
    }catch(error){
      this.$store.dispatch("toast/error", {message: "Could not load Project Evaluation", error})
    }
  },

}
</script>