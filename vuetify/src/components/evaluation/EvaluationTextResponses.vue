<style scoped>
  .quote{
    border-left: 4px solid lightgray;
    margin-bottom: 16px;
    padding: 8px 12px !important;
  }
  .quote div:last-child{
    margin-bottom: -16px;
  }
</style>

<template>
  <v-card v-if="textResponses.length > 0">
    <v-card-title>
      <h2 class="title">
        {{ $t('pages.evaluationDetail.commentsByParticipants') }}
      </h2>
    </v-card-title>
    <v-card-text>
      <v-sheet :max-height="400" style="overflow-y:auto; overflow-x:hidden">
        <v-layout ma-0 pa-0 wrap>

          <!-- Single participant quote -->
          <v-flex v-for="response in textResponses" :key="response.id" class="quote" xs12>
            <small class="text-uppercase">
              <strong>{{ question(response.question).name }}</strong>
            </small>
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
      return this.$store.getters['evaluation/responses'].filter(r => r.answer_text.length > 5)
    },
  },

  methods: {
    question(questionId){
      return this.$store.getters['evaluation/questions'].filter(q => q.id == questionId)[0]
    }
  },

  async created() {
    // Load evaluations
    try{
      await this.$store.dispatch("evaluation/loadResponses", {
        limit: 1000,
        project: this.projectId,
        answer_type: "TEXT"
      })
      await this.$store.dispatch("evaluation/loadQuestions", {limit: 1000})
    }catch(error){
      // this.$store.dispatch("toast/error", {message: this.$t('forms.toasts.permissionError'), error})
      // nothing, user does not have permission to view responses
    }
  },

}
</script>