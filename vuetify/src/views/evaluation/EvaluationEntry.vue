<style>
table{
  width: 100%;
}
table td, table th{
  padding: 0 8px 8px 8px;
}
table th{
  text-align: right;
}

.v-input .accent--text{
  color: #00796b !important; /* primary */
}
</style>

<template>

  <v-layout v-if="project.id" row wrap align-content-start>
    <v-flex xs12>
      <h1 class="mb-2">
        {{ $t('pages.evaluationEntry.mainTitle') }}
      </h1>
      <h2>
        <small>{{ $t('noums.project') }}:</small>
        {{ project.name }}
      </h2>
    </v-flex>


    <!-- Not validated Alert -->
    <v-flex v-if="isCompleted" xs12>
      <v-alert color="success" :value="true" class="subheading">
        <v-icon dark left>
          check
        </v-icon>&nbsp;
        {{ $t('pages.evaluationEntry.questionnaireCompleted') }}
      </v-alert>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            {{ $t('pages.evaluationEntry.evaluationOverview') }}
          </h2>

          <v-layout row wrap py-3>
            <!-- table col 1 -->
            <v-flex xs12 sm6 py-0>
              <table>
                <tr>
                  <th>{{ $t('noums.project') }}</th>
                  <td>{{ project.name }}</td>
                </tr>
                <tr>
                  <th>{{ $t('pages.evaluationEntry.evaluatedPhase') }}</th>
                  <td>{{ $t(phase(evaluation.project_phase).name) }}</td>
                </tr>
              </table>
            </v-flex>
            <!-- Table col 2 -->
            <v-flex xs12 sm6 py-0>
              <table>
                <tr>
                  <th>{{ $t('pages.evaluationEntry.evaluator') }}</th>
                  <td>{{ evaluationUser.full_name }}</td>
                </tr>
                <tr>
                  <th>{{ $t('pages.evaluationEntry.evaluationRole') }}</th>
                  <td>{{ $t(role(evaluation.role).name) }}</td>
                </tr>
              </table>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex v-if="evaluation.project_phase == 1" xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            {{ $t('pages.evaluationEntry.selfQuestionnaireTitle') }}
          </h2>
          {{ $t('pages.evaluationEntry.selfQuestionnaireDescription') }}

          <p class="text-xs-center">
            <v-btn large dark color="red" href="https://app.inspiresproject.com/uploads/inspires-self-questionaire.pdf" target="_blank">
              <v-icon left>
                mdi-file-pdf
              </v-icon>
              {{ $t('actions.downloadName', {name: $t('pages.evaluationEntry.selfQuestionnaireTitle')}) }}
            </v-btn>
          </p>
        </v-card-text>
        <p />
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            {{ $t(`models.projectPhase.phase${evaluation.project_phase}`) }}
          </h2>
          {{ $t(`models.projectPhase.phase${evaluation.project_phase}Description`) }}
          <p />
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            {{ $t('pages.evaluationEntry.questionnaire') }}
          </h2>

          <vue-markdown>{{ $t('pages.evaluationEntry.questionnaireDescription') }}</vue-markdown>

          <v-form ref="form">
            <template v-for="(question, qidx) in questions">
              <!-- MULTIPLE questions -->
              <div v-if="question.answer_type == 'MULTIPLE'" :key="question.id">
                <h3 class="mt-4">
                  {{ $t(`models.question.${question.id}`) }} {{ $t('pages.evaluationEntry.questionMultipleHelp') }}
                </h3>

                <v-checkbox v-for="(answer, aidx) in question.answers" :key="aidx"
                            v-model="answers[qidx]"
                            :value="answer.key"
                            :label="answer.name"
                            hide-details
                />
              </div>
              <!-- /MULTIPLE QUESTIONS -->

              <!-- DEGREE Questions -->
              <div v-else-if="question.answer_type == 'DEGREE'" :key="question.id">
                <h3 class="mt-4">
                  {{ $t(`models.question.${question.id}`) }}
                </h3>

                <v-slider
                  v-model="answers[qidx]"
                  :thumb-color="answers[qidx] > 4 ? 'teal' : answers[qidx] > 2 ? 'teal lighten-1' : 'teal lighten-2'"
                  :readonly="!canModify"
                  always-dirty
                  thumb-label="always"
                  class="px-4 mt-5"
                  step="1"
                  min="0"
                  tick-size="4"
                  :tick-labels="'01234567'.split('')"
                  :max="question.answer_range"
                />
              </div>
              <!-- /DEGREE Questions -->

              <!-- TEXT Questions -->
              <div v-else-if="question.answer_type == 'TEXT'" :key="question.id">
                <h3 class="mt-4 mb-3">
                  {{ $t(`models.question.${question.id}`) }}
                  {{ $t('models.question.Q10XY', {phase: $t(phase(evaluation.project_phase).tag)}) }}
                </h3>

                <v-textarea
                  v-model="answers[qidx]"
                  outline
                  single-line
                  counter="500"
                  auto-grow
                  rows="4"
                />
              </div>
              <!-- /TEXT Questions -->
            </template>


            <v-btn v-if="canModify && !isCompleted" block large color="success"
                   class="mt-5"
                   @click="attemptSubmit()"
            >
              {{ $t('actions.submit') }}
            </v-btn>

            <v-btn v-else-if="canModify" block large color="success"
                   class="mt-5"
                   @click="attemptSubmit()"
            >
              {{ $t('actions.updateResponse') }}
            </v-btn>

            <v-btn v-else block large color="primary"
                   class="mt-5" disabled
            >
              {{ $t('pages.evaluationEntry.viewOnly') }}
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>

  <v-layout v-else row wrap align-content-start>
    <v-flex xs12>
        <h1 class="title">{{ $t('actions.loading') }}...</h1>
        <br>
        <p>{{ message }}</p>
    </v-flex>
  </v-layout>

</template>

<script>
export default {

  metaInfo(){
    return {
      title: this.$t("pages.evaluationEntry.mainTitle")
    }
  },
  data(){
    return{
      message: '',
      questions: [],
      /** Multi-type array of answers, contains DEGREE, MULTIPLE CHOICE, TEXT... */
      answers:          [],
    }
  },

  computed:{
    evaluationId(){
      return this.$route.params.slug
    },
    evaluation(){
      return this.$store.getters['evaluation/detail'](this.evaluationId)
    },
    project(){
      return this.$store.getters['project/detail'](this.evaluation.project)
    },

    currentUser(){
      return this.$store.getters['user/current']
    },
    evaluationUser(){
      let participation = this.project.participants
        .filter(part => part.id == this.evaluation.participation)[0]
      return this.$store.getters['user/get'](participation.user)
    },
    canModify(){
      let isSameUser = this.currentUser.id == this.evaluationUser.id
      return isSameUser || this.currentUser.is_administrator
    },

    isCompleted(){
      return this.evaluation.responses.length > 0
    },

    computedAnswers(){
      return this.questions.map( (q, idx) =>
        ({
          question: q.id,
          response: this.answers[idx]
        })
      )
    }
  },

  async created(){
    // Retrieve data
    try{
      await this.$store.dispatch("evaluation/load", [this.evaluationId])
      await this.$store.dispatch("project/load", [this.evaluation.project])
    }catch(error){
      this.$store.dispatch("toast/error", {
        message:this.$t('forms.toasts.permissionError'),
        error
      })
      this.message = this.$t('forms.toasts.permissionError');
      return;
    }

    // Copy the evaluation questions sorting by id minus the 'Q'
    this.questions = this.evaluation.questions.slice().sort((a,b) =>{
      let aId = parseInt(a.id.replace('Q',''))
      let bId = parseInt(b.id.replace('Q',''))
      return aId - bId;
    })

    // Load existing responses
    let loadedAnswers = []
    this.questions.forEach((question, idx) => {
      let response = this.getResponse(question.id)

      // Init default values on array
      if(question.answer_type == "DEGREE") { loadedAnswers[idx] = 0 }
      if(question.answer_type == "MULTIPLE") { loadedAnswers[idx] = [] }
      if(question.answer_type == "TEXT") { loadedAnswers[idx] = "" }

      if(response){
        if(question.answer_type == "DEGREE") { loadedAnswers[idx] = response.answer_degree }
        if(question.answer_type == "MULTIPLE") { loadedAnswers[idx] = response.answer_multiple }
        if(question.answer_type == "TEXT") { loadedAnswers[idx] = response.answer_text }
      }
    });

    this.answers = [...loadedAnswers]
  },

  methods: {
    phase(id){
      return this.$store.getters['evaluation/phases'][id]
    },
    role(id){
      return this.$store.getters['evaluation/roles'][id]
    },
    user(id){
      return this.$store.getters["user/get"](id)
    },

    getParticipant(participationId){
      return this.project.participants.filter(part => part.id == participationId)
    },

    getResponse(questionId){
      return this.evaluation.responses.filter(r => r.question == questionId)[0]
    },

    getResponseTypeField(responseTypeEnum){
      return 'answer_' + responseTypeEnum.toLowerCase()
    },

    async attemptSubmit(){
      let form = this.$refs.form

      try{
        // Try to submit answers
        for (let i = 0; i < this.computedAnswers.length; i++) {
          const answer = this.computedAnswers[i];

          // get response type
          let responseType = this.getResponseTypeField(this.questions[i].answer_type)
          let oldResponse = this.getResponse(answer.question) || {}

          let response = {
            "id": oldResponse.id,
            "evaluation": this.evaluationId,
            "question": answer.question,
            [responseType]: answer.response,
          }

          console.log(response)

          await this.$store.dispatch("evaluation/submitResponse", response)
        }

        await this.$store.dispatch("evaluation/load", [this.evaluationId])
        this.$store.dispatch("toast/success", this.$t("pages.evaluationEntry.submitSuccess"))

      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.evaluationEntry.submitFailure"),
          error
        })
      }

    }
  }
};
</script>
