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
  <v-layout row wrap align-content-start v-if="project.id">
    <v-flex xs12>
      <h1> {{ $t('pages.evaluationEntry.mainTitle') }}</h1>
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
                  <td>{{ role(evaluation.role).name }}</td>
                </tr>
              </table>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
             {{ $t(`models.projectPhase.phase${evaluation.phase}`) }}
          </h2>
             {{ $t(`models.projectPhase.phase${evaluation.phase}Description`) }}
          <p></p>

        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            {{ $t('pages.evaluationEntry.questionnaire') }}
          </h2>
          <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ipsum, autem delectus ea est dolore animi adipisci voluptas fugit omnis labore facere, repellat dolorum culpa unde repudiandae corrupti odit voluptates blanditiis.</p>

          <v-form ref="form">

            <template v-for="(question, qidx) in evaluation.questions">

              <!-- MULTIPLE questions -->
              <div v-if="question.answer_type == 'MULTIPLE'" :key="question.id">
                <h3 class="mt-4">
                  {{ question.name }} {{ $t('pages.evaluationEntry.questionMultipleHelp') }}
                </h3>
                <v-btn disabled flat outline small style="color:#888 !important">
                  {{ role(question.role).name }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#888 !important">
                  {{ $t(phase(question.phase).tag) }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#888 !important">
                  {{ question.principle }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#888 !important">
                  {{ question.dimension }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#888 !important">
                  {{ question.axis }}
                </v-btn>
                <v-checkbox v-for="(answer, aidx) in question.answers" :key="aidx"
                  v-model="answersMultiple[qidx]"
                  :value="answer.key"
                  :label="answer.name"
                  hide-details
                />
              </div>
              <!-- /MULTIPLE QUESTIONS -->

              <!-- DEGREE Questions -->
              <div v-else-if="question.answer_type == 'DEGREE'" :key="question.id">
                <h3 class="mt-4">
                  {{ question.name }}
                </h3>

                <v-btn disabled flat outline small style="color:#999 !important">
                  {{ role(question.role).name }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#999 !important">
                  {{ $t(phase(question.phase).tag) }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#999 !important">
                  {{ question.principle }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#999 !important">
                  {{ question.dimension }}
                </v-btn>
                <v-btn disabled flat outline small style="color:#999 !important">
                  {{ question.axis }}
                </v-btn>

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

            </template>


            <v-btn block large color="success" class="mt-5"
              v-if="canModify && !isCompleted"
              @click="attemptSubmit()">
              {{ $t('actions.submit') }}
            </v-btn>

            <v-btn block large color="success" class="mt-5"
              v-else-if="canModify"
              @click="attemptSubmit()">
              {{ $t('actions.updateResponse') }}
            </v-btn>

            <v-btn block large color="primary" class="mt-5"
              disabled v-else>
              {{ $t('pages.evaluationEntry.viewOnly') }}
            </v-btn>

          </v-form>


        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default {

  metaInfo:{
    title: "Project Evaluation"
  },

  data(){
    return{
      answers:          [],
      answersMultiple:  [[],[],[],[],[],[],[],[],[]]
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
      let isSuperUser = this.currentUser.id == 1
      return isSameUser || isSuperUser
    },

    isCompleted(){
      return this.evaluation.responses.length > 0
    },


    computedAnswers(){
      return this.evaluation.questions.map( (q, idx) =>{
        if(q.answer_type == "MULTIPLE"){
          return ({
            question:q.id,
            response: this.answersMultiple[idx]
          })
        }
        if(q.answer_type == "DEGREE"){
          return ({
            question:q.id,
            response: this.answers[idx] || 0
          })
        }
        throw new Error("unidentified answer type")
      })
    }
  },

  async created(){
    await this.$store.dispatch("evaluation/load", [this.evaluationId])
    await this.$store.dispatch("project/load", [this.evaluation.project])

    // Load existing responses
    let loadedAnswers = []
    this.evaluation.questions.forEach((question, idx) => {
      let response = this.getResponse(question.id)
      if(response){
        if(question.answer_type == "DEGREE") { loadedAnswers[idx] = response.answer_degree }
        if(question.answer_type == "MULTIPLE") { loadedAnswers[idx] = response.answer_multiple }
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

    async attemptSubmit(){
      let form = this.$refs.form

      try{
        // Try to submit answers
        for (let i = 0; i < this.computedAnswers.length; i++) {
          const answer = this.computedAnswers[i];

          // Infer response type
          let responseType
          if (Array.isArray(answer.response)){ responseType = "answer_multiple" }
          else{ responseType = "answer_degree" }

          let oldResponse = this.getResponse(answer.question) || {}

          let response = {
            "id": oldResponse.id,
            "evaluation": this.evaluationId,
            "question": answer.question,
            [responseType]: answer.response,
          }

          await this.$store.dispatch("evaluation/submitResponse", response)
        }

        await this.$store.dispatch("evaluation/load", [this.evaluationId])
        this.$store.dispatch("toast/success", this.$t("pages.evaluationEntry.submitSuccess"))

      }catch(err){
        this.$store.dispatch("toast/error", this.$t("pages.evaluationEntry.submitFailure"))
      }

    }
  }
};
</script>
