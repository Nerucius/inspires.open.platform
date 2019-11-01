<style scoped>
  .quote > div{
    border-left: 4px solid lightgray;
    padding: 4px 0px 2px 12px;
  }
  .v-card__text{
    /* Hide graphs going out of cards */
    overflow: hidden;
  }
</style>

<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex xs12>
      <h1> {{ $t('noums.evaluation') }} | {{ project.name }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-layout id="target-graph-area" row wrap>
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('pages.evaluationDetail.projectOverallPosition') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text id="reference-width">
              <v-sheet height="200">
                <div id="scatterchart" />
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('pages.evaluationDetail.projectEvolution') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-sheet height="200">
                <div id="linechart" />
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat style="background-color:#2F4193">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.transform') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="transfchart" />
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.CollectiveCapacity') }}</h3>
                <div id="TransformativeCollectiveChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.knowledgeAndSkills') }}</h3>
                <div id="TransformativeSkillsChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.policyImpact') }}</h3>
                <div id="TransformativePolicyChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.selfImprovement') }}</h3>
                <div id="TransformativeSelfChart" />
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat style="background-color:#2599D4">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.knowledge') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="knowchart" />
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.openness') }}</h3>
                <div id="KnowledgeOpennessChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.scientificRelevance') }}</h3>
                <div id="KnowledgeRelevanceChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.transdisciplinarity') }}</h3>
                <div id="KnowledgeTransdisciplChart" />
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="yellow darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.participation') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="partchart" />
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.degreeOfEngagement') }}</h3>
                <div id="ParticipatoryEngagementChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.impactParticipatoryDynamics') }}</h3>
                <div id="ParticipatoryImpactChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.motivation') }}</h3>
                <div id="ParticipatoryMotivationChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.satisfactionParticipatoryDynamics') }}</h3>
                <div id="ParticipatorySatisfactionChart" />
              </div>
            </v-card-text>
          </v-card>
        </v-flex>


        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="orange darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.integrity') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="integchart" />
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.expectationAlignment') }}</h3>
                <div id="IntegrityExpectationChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.genderPerspective') }}</h3>
                <div id="IntegrityGenderChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.inclusivity') }}</h3>
                <div id="IntegrityInclusivityChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.reflexivity') }}</h3>
                <div id="IntegrityReflexivityChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.resourceAvailability') }}</h3>
                <div id="IntegrityResourceChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.transparency') }}</h3>
                <div id="IntegrityTransparencyChart" />
              </div>
            </v-card-text>
          </v-card>
        </v-flex>


        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="teal darken-2">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.citizen') }}
                </h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="citizchart" />
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.communityAlignment') }}</h3>
                <div id="CitizenCommunityChart" />
              </div>
              <div class="bullet">
                <h3>{{ $t('models.evaluation.dimension.responsivenessCommunityAlignment') }}</h3>
                <div id="CitizenResponsivenessChart" />
              </div>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-flex>

    <v-flex xs12>
      <EvaluationTextResponses :project-id="projectId" />
    </v-flex>

  </v-layout>
</template>

<script>
import EvaluationTextResponses from "@/components/evaluation/EvaluationTextResponses";

import { createParticipantGraph } from "@/plugins/vega.evaluation";
import { slug2id, obj2slug } from "@/plugins/utils";
import { API_SERVER } from '@/plugins/resource';
import { debounce } from "lodash";

export default {
  metaInfo() {
    return {
      title: this.$t('noums.evaluation') + " " + (this.project || {}).name
    };
  },

  components:{
    EvaluationTextResponses
  },

  data() {
    return {
      obj2slug,
      project: null,
    };
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    evaluations(){
      return this.$store.getters['evaluation/project'](this.projectId);
    },
    isApprovedProject() {
      return (
        this.project.collaboration != null &&
        this.project.collaboration.is_approved
      );
    }
  },

  async created() {
    try {
      // Load project
      await this.$store.dispatch("project/load", [this.projectId]);
      this.project = this.$store.getters["project/detail"](this.projectId);

    } catch (error) {
      this.$store.dispatch("toast/error", {message: "Could not load Project", error})
    }

    window.addEventListener("resize", this.onResize);

    setTimeout(() => {
      this.createGraph()
    }, 300);

  },

  methods: {
    onResize(event){
      this.createGraph()
    },

    createGraph: debounce( function () {
      let width = document.querySelector("#reference-width").clientWidth
      createParticipantGraph(this.projectId, width)
    }, 750, {leading: false, trailing: true}),

    user(uid) {
      return this.$store.getters["user/get"](uid);
    },

    role(rid) {
      return this.$store.getters["evaluation/roles"][rid];
    }
  }
};
</script>


<style scoped>

.title{
  font-size: 100% !important;
  font-weight: bold;
}

.vega-embed{
  padding:0;
}

.bullet{
  display: flex;
  align-items: center
}

.bullet h3{
  flex: 1 0 0;
  flex-basis: 120px;
  flex-grow: 0;
  flex-shrink: 0;
  font-size: 100%;
  overflow: hidden;
  padding-bottom: 20px;
}



/* hr {
  margin-top: -10px;
  width: 405px;
  float: left;
}
h2 {
  margin-top: 20px;
  height: 2em;
  font-size: 1.2em;
}
h3 {
  width: 120px;
  height: 40px;
  line-height: 1.1em;
  font-size: 0.9em;
  margin: 0;
  padding: 0.9em 0 0 0;
  float: left;
}
.bullet {
  width: 100%;
  padding: 0;
  margin: 0;
}
.vega-embed {
  width: 280px;
  padding-right: 0 !important;
  margin: 0;
}
#main {
  display: grid;
  grid-template-columns: 40px 400px 40px 400px 40px;
  grid-template-rows: 60px 280px auto;
}
#scatter {
  grid-column-start: 2;
  grid-column-end: 3;
  grid-row-start: 2;
}
#line {
  grid-column-start: 4;
  grid-column-end: 5;
  grid-row-start: 2;
}
#transf {
  grid-column-start: 2;
  grid-column-end: 3;
  grid-row-start: 3;
}
#heat {
  grid-column-start: 4;
  grid-column-end: 5;
  grid-row-start: 3;
} */
</style>
