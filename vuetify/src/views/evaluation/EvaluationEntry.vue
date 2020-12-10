<style scoped>
/* Styles affecting the router-view content (this page) */

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

small{
  color:darkslategray;
  background-color: lightgray;
  border-radius: 5px;
  padding: 3px;
  margin-right: 8px;
}
</style>

<style>
/* Styles affecting the entire page, not just this component */

  .theme--light.v-label{
    color:rgba(0, 0, 0, 0.85) !important
  }

  .media-print{
    display: none;
}

@media print {

  nav{
    display: none !important;
  }
  #footer{
    display: none !important;
  }

  .media-screen{
    display: none;
  }
  .media-print {
    display: inherit;
  }

  .v-content{
    padding: 0;
    margin: 0;
  }

  #self-questionnaire{
    display: none;
  }
  #project-phase{
    display: none;
  }
}
</style>

<template>
  <v-layout v-if="project.id" row wrap align-content-start>
    <v-flex xs12>
      <h1>
        {{ project.name }}
      </h1>
      <h2 class="mt-2">
        {{ $t('pages.evaluationEntry.mainTitle') }}
      </h2>
    </v-flex>


    <!-- Completed Dialog -->
    <v-flex v-if="isCompleted" xs12>
      <v-alert color="success" :value="true" class="subheading">
        <v-icon dark left>
          check
        </v-icon>&nbsp;
        {{ $t('pages.evaluationEntry.questionnaireCompleted') }}
      </v-alert>
    </v-flex>


    <!-- Eval token -->
    <v-flex v-if="!!this.$route.query.eval_token" xs12>
      <v-alert color="info" :value="true" class="subheading">
        <v-layout align-center>
        <v-flex shrink>
          <v-icon dark>info</v-icon>
        </v-flex>
        <v-flex>
          <p>{{ $t('pages.evaluationEntry.answeringAsToken', {name:evaluationUser.full_name}) }}</p>
          {{ $t('pages.evaluationEntry.manageProfileLink') }} <v-btn outline flat color="white" :to="{name:'login', query:{'token': $route.query.eval_token}}">{{$t('toolbar.myAccount')}}</v-btn>
        </v-flex>
        </v-layout>
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
                <colgroup>
                  <col style="width:40%">
                  <col>
                </colgroup>
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
                <colgroup>
                  <col style="width:40%">
                  <col>
                </colgroup>
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

    <v-flex v-if="evaluation.project_phase == 1" id="self-questionnaire" xs12>
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

    <v-flex id="project-phase" xs12>
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
              <!-- MULTIPLE ANSWER questions -->
              <div v-if="question.answer_type == 'MULTIPLE'" :key="question.id">
                <h3 class="mt-4">
                  <small>{{ question.id }}</small>
                  {{ $t(`${question.i18n}`) }} {{ $t('pages.evaluationEntry.questionMultipleHelp') }}
                </h3>

                <v-layout row wrap mb-5>
                  <v-flex v-for="(answer, aidx) in question.answers" :key="aidx" xs12 sm6 py-0>
                    <v-checkbox
                      v-model="answers[qidx]"
                      :value="answer.key"
                      :label="answer.name"
                      hide-details
                    />
                  </v-flex>
                </v-layout>
              </div>
              <!-- /MULTIPLE ANSWER QUESTIONS -->

              <!-- DEGREE Questions -->
              <div v-else-if="question.answer_type == 'DEGREE'" :key="question.id">
                <h3 class="mt-4">
                  <small>{{ question.id }}</small>
                  {{ $t(`${question.i18n}`) }}
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
                  <small>{{ question.id }}</small>
                  {{ $t(`${question.i18n}`) }}
                  <br/>
                  <br/>
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


            <div class="media-screen">
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
            </div>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>

  <v-layout v-else row wrap align-content-start>
    <v-flex xs12>
      <h1 class="title">
        {{ $t('actions.loading') }}...
      </h1>
      <br>
      <p>{{ message }}</p>
    </v-flex>
  </v-layout>
</template>

<script>
import Cookies from 'js-cookie'

export default {

  metaInfo(){
    return {
      title: this.$t("pages.evaluationEntry.mainTitle")
    }
  },

  data(){
    return{
      headers: null,
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
      // Override for token links
      if(!!this.$route.query.user_id)
        return this.$store.getters['user/get'](this.$route.query.user_id)
      return this.$store.getters['user/current']
    },
    evaluationUser(){
      let participation = this.project.participants
        .filter(part => part.id == this.evaluation.participation)[0]
      return this.$store.getters['user/get'](participation.user)
    },
    canModify(){
      let isSameUser = this.currentUser.id == this.evaluationUser.id
      return isSameUser || this.currentUser.is_superuser || this.project.isManager(this.currentUser.id)
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
      // Detect evaluation token and save to custom headers
      if(this.$route.query.eval_token){
        this.headers = {'Authorization':'Token '+this.$route.query.eval_token}
      }

      // Retrieve data
      try{
        await this.$store.dispatch("evaluation/load", {id: this.evaluationId, headers:this.headers})
        await this.$store.dispatch("project/load", [this.evaluation.project])
      }catch(error){
        this.$store.dispatch("toast/error", {
          message:this.$t('forms.toasts.permissionError'),
          error
        })
        this.message = this.$t('forms.toasts.permissionError');
        return;
      }
    // }


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

    getResponse(questionId){
      return this.evaluation.responses.filter(r => r.question == questionId)[0]
    },

    getResponseTypeField(responseTypeEnum){
      return 'answer_' + responseTypeEnum.toLowerCase()
    },

    async attemptSubmit(){
      let form = this.$refs.form

      // Construct responses array
      let responses = [];
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

        responses.push(response)
      }

      // Try to submit answers
      try{
        await Promise.all(responses.map(response => this.$store.dispatch('evaluation/submitResponse', {response, headers:this.headers})))
        this.$store.dispatch("evaluation/load", {id: this.evaluationId, headers:this.headers})
        this.$store.dispatch("toast/success", this.$t("pages.evaluationEntry.submitSuccess"))

      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.evaluationEntry.submitFailure"),
          error
        })
      }

      if(!this.isCompleted){
        // Evaluation submit event for the first time
        this.$matomo && this.$matomo.trackEvent('evaluation', 'evaluation--submit')
      }

    }
  }
};
</script>
