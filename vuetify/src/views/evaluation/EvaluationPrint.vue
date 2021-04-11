<style scoped>
  /* Styles affecting the router-view content (this page) */

  table {
    width: 100%;
  }
  table td,
  table th {
    padding: 0 8px 8px 8px;
  }
  table th {
    text-align: left;
  }

  .v-input .accent--text {
    color: #00796b !important; /* primary */
  }

  .nobreak{
    white-space: nowrap;
  }

  small {
    color: darkslategray;
    background-color: lightgray;
    border-radius: 5px;
    padding: 3px;
    margin-right: 8px;
  }
</style>

<style>
  /* Styles affecting the entire page, not just this component */

  .theme--light.v-label {
    color: rgba(0, 0, 0, 0.85) !important;
  }

  .media-print {
    display: none;
  }

  @media print {

    .application{
      background: none !important;
    }

    .no-page-break{
      page-break-inside: avoid
    }

    /* Remove Navigation bar padding */
    .v-content__wrap {
      margin-top: -56px !important;
    }

    nav {
      display: none !important;
    }
    #footer {
      display: none !important;
    }

    .container {
      padding: 12px
    }

    .media-screen {
      display: none;
    }
    .media-print {
      display: inherit;
    }

    .v-text-field{
      padding: 0
    }


    small {
      border: 1px solid darkslategray;
      background: none !important;
    }

    #self-questionnaire {
      display: none;
    }
    #project-phase {
      display: none;
    }
  }
</style>

<template>
  <v-layout row wrap align-content-start justify-end>
    <v-flex xs12 class="media-screen">
      <v-btn color="grey darken-3" block dark @click="printPage">
        <v-icon left>print</v-icon>
        {{ $t('actions.print') }}
      </v-btn>
    </v-flex>

    <!-- Evaluation Overview -->
    <v-flex xs12>
      <v-card flat>
        <v-card-text class="pa-0">
          <h2 class="mb-2">
            {{ $t("noums.evaluation") }}
          </h2>

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
            <tr>
              <th>{{ $t('forms.fields.role') }}</th>
              <td>{{ $t(role(evaluation.role).name) }}</td>
            </tr>
            <tr>
              <th>{{ $t('forms.fields.firstName') }}</th>
              <td>
                <v-text-field single-line hide-details readonly />
              </td>
            </tr>
            <tr>
              <th>{{ $t('forms.fields.lastName') }}</th>
              <td>
                <v-text-field single-line hide-details readonly />
              </td>
            </tr>
            <tr><td colspan="2">&nbsp;</td></tr>
            <tr>
              <th>{{ $t('forms.fields.genderIdentity') }}</th>
              <td>
                <v-layout wrap justify-space-between>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.userGender.male') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.userGender.female') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.userGender.other') }}<br>
                  </v-flex>
                </v-layout>
              </td>
            </tr>
            <tr><td colspan="2">&nbsp;</td></tr>
            <tr>
              <th>{{ $t('forms.fields.education') }}</th>
              <td>
                <v-layout wrap justify-space-between>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.educationLevel.primary') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.educationLevel.secondary') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.educationLevel.tertiary') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.educationLevel.degree') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.educationLevel.master') }}<br>
                  </v-flex>
                  <v-flex shrink>
                    <v-icon>mdi-circle-outline</v-icon> {{ $t('models.educationLevel.doctoral') }}<br>
                  </v-flex>
                </v-layout>

              </td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </v-flex>

    <!-- Questions -->
    <v-flex xs12>
      <v-card flat>
        <v-card-text class="pa-0">
          <h2 class="mb-2">
            {{ $t('pages.evaluationEntry.questionnaire') }}
          </h2>
          <template v-for="question in questions">
            <!-- DEGREE Questions -->
            <div v-if="question.answer_type == 'DEGREE'" :key="question.id" class="no-page-break mb-4">
              <h3>
                <small>{{ question.id }}</small>
                {{ $t(`${question.i18n}`) }}
              </h3>

              <v-layout row justify-space-around>
                <v-flex v-for="i in '01234567'"
                        :key="i" shrink
                        class="text-xs-center"
                >
                  <v-icon>mdi-circle-outline</v-icon><br>
                  <b>{{ i }}</b>
                </v-flex>
              </v-layout>
            </div>
            <!-- /DEGREE Questions -->

            <!-- MULTIPLE ANSWER QUESTIONS -->
            <div v-if="question.answer_type == 'MULTIPLE'" :key="question.id" class="no-page-break mt-5">
              <h3>
                <small>{{ question.id }}</small>
                {{ $t(`${question.i18n}`) }} {{ $t('pages.evaluationEntry.questionMultipleHelp') }}
              </h3>

              <v-layout row wrap px-3>
                <v-flex v-for="i in '123456789'" :key="i" xs12 sm6 py-0>
                  <v-checkbox
                    :label="tAnswer(i)"
                    hide-details
                  />
                </v-flex>
              </v-layout>
            </div>
            <!-- /MULTIPLE ANSWER QUESTIONS -->

            <!-- TEXT Questions -->
            <div v-if="question.answer_type == 'TEXT'" :key="question.id" class="no-page-break mt-5">
              <h3 class="">
                <small>{{ question.id }}</small>
                {{ $t(`${question.i18n}`) }}
                <br>
                <br>
                {{ $t('models.question.Q10XY', {phase: $t(phase(evaluation.project_phase).tag)}) }}
              </h3>

              <v-textarea
                outline
                single-line
                rows="4"
                hide-details
              />
            </div>
            <!-- /TEXT Questions -->
          </template>
        </v-card-text>
      </v-card>
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
      headers: null,
      message: '',
      evaluation: {},
    }
  },

  computed:{
    computedAnswers(){
      return this.questions.map( (q, idx) =>
        ({
          question: q.id,
          response: this.answers[idx]
        })
      )
    },
    project(){
      return this.$store.getters['project/detail'](this.$route.query.project)
    },
    questions(){
      return this.$store.getters['evaluation/questions']
    },
  },

  async created(){
    // Detect evaluation token and save to custom headers
    this.evaluation = {
        role: this.$route.query.role,
        project_phase: this.$route.query.phase,
    }

    // Retrieve data
    try{
      await this.$store.dispatch("project/load", [this.$route.query.project])
      await this.$store.dispatch("evaluation/loadQuestions", {...this.$route.query})

    }catch(error){
      this.$store.dispatch("toast/error", {
        message:this.$t('forms.toasts.error'),
        error
      })
    }



    // Copy the evaluation questions sorting by id minus the 'Q'
    // this.questions = this.evaluation.questions.slice().sort((a,b) =>{
    //   let aId = parseInt(a.id.replace('Q',''))
    //   let bId = parseInt(b.id.replace('Q',''))
    //   return aId - bId;
    // })

  },

  methods: {
    phase(id){
      return this.$store.getters['evaluation/phases'][id]
    },
    role(id){
      return this.$store.getters['evaluation/roles'][id]
    },

    tAnswer(key){
      return this.$t(`models.answer.A0${key}`)
    },

    getResponse(questionId){
      return this.evaluation.responses.filter(r => r.question == questionId)[0]
    },

    getResponseTypeField(responseTypeEnum){
      return 'answer_' + responseTypeEnum.toLowerCase()
    },

    printPage(){
      window.print()
    }

  }
};
</script>
