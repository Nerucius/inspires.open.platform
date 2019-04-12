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
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>Evaluation Questionaire</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            Objective
          </h2>
          <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ipsum, autem delectus ea est dolore animi adipisci voluptas fugit omnis labore facere, repellat dolorum culpa unde repudiandae corrupti odit voluptates blanditiis.</p>
          <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Commodi, molestiae earum ea, ex aliquam necessitatibus quo fugiat eos sunt rem reiciendis labore tempore voluptates odio saepe quod ad a at! Lorem ipsum dolor, sit amet consectetur adipisicing elit. Molestias fuga ratione cupiditate voluptate eligendi repudiandae, quae minus a reiciendis id quod facilis tempora similique. Perferendis blanditiis suscipit consequatur quo ipsam!</p>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h2 class="mb-2">
            Evaluation Overview
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
                  <th>Evaluated Phase</th>
                  <td>{{ $t(phase(evaluation.project_phase).name) }}</td>
                </tr>
              </table>
            </v-flex>
            <!-- Table col 2 -->
            <v-flex xs12 sm6 py-0>
              <table>
                <tr>
                  <th>Evaluator</th>
                  <!-- TODO: Add user to API and pull info here -->
                  <td>{{ $store.getters['user/current'].full_name }}</td>
                </tr>
                <tr>
                  <th>Evaluation Role</th>
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
            Questionaire
          </h2>
          <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Ipsum, autem delectus ea est dolore animi adipisci voluptas fugit omnis labore facere, repellat dolorum culpa unde repudiandae corrupti odit voluptates blanditiis.</p>


          <template v-for="(question, qidx) in evaluation.questions">
            <!-- MULTIPLE questions -->
            <div v-if="question.answer_type == 'MULTIPLE'" :key="question.id">
              <h3 class="mt-4">
                {{ question.name }} (choose all that apply)
              </h3>
              <v-btn disabled flat outline small style="color:#888 !important"> {{ role(question.role).name }} </v-btn>
              <v-btn disabled flat outline small style="color:#888 !important"> {{ $t(phase(question.phase).tag) }} </v-btn>
              <v-btn disabled flat outline small style="color:#888 !important"> {{ question.principle }} </v-btn>
              <v-btn disabled flat outline small style="color:#888 !important"> {{ question.dimension }} </v-btn>
              <v-btn disabled flat outline small style="color:#888 !important"> {{ question.axis }} </v-btn>
              <v-checkbox v-for="(answer,idx) in question.answers" :key="idx" hide-details
                          :label="answer.name"
              />
            </div>
            <!-- DEGREE Questions -->
            <div v-else-if="question.answer_type == 'DEGREE'" :key="question.id">
              <h3 class="mt-4">
                {{ question.name }}
              </h3>

              <v-btn disabled flat outline small style="color:#999 !important"> {{ role(question.role).name }} </v-btn>
              <v-btn disabled flat outline small style="color:#999 !important"> {{ $t(phase(question.phase).tag) }} </v-btn>
              <v-btn disabled flat outline small style="color:#999 !important"> {{ question.principle }} </v-btn>
              <v-btn disabled flat outline small style="color:#999 !important"> {{ question.dimension }} </v-btn>
              <v-btn disabled flat outline small style="color:#999 !important"> {{ question.axis }} </v-btn>

              <v-slider
                v-model="answers[qidx]"
                :thumb-color="answers[qidx] > 4 ? 'green' : answers[qidx] > 2 ? 'orange' : 'red'"
                always-dirty
                thumb-label="always"
                class="px-4 mt-5"
                step=1
                min=0
                tick-size="4"
                :tick-labels="'01234657'.split('')"
                :max="question.answer_range"
              />
            </div>
          </template>


          <v-btn block large color="success"
            class="mt-5"
            @click="attemptSubmit()"
          >
            {{ $t('actions.save') }}
          </v-btn>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default {

  metaInfo:{
    title: "Evaluation"
  },

  components:{
  },

  data(){
    return{
      answers:[]
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
  },

  async mounted(){
    await this.$store.dispatch("evaluation/load", [this.evaluationId])
    await this.$store.dispatch("project/load", [this.evaluation.project])
  },

  methods: {
    phase(id){
      return this.$store.getters['evaluation/phases'][id]
    },
    role(id){
      return this.$store.getters['evaluation/roles'][id]
    },
    attemptSubmit(){
      this.$store.dispatch("toast/error", "Evaluation saving not implemented yet.")
    }
  }
};
</script>
