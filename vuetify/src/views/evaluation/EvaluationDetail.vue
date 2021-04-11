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
    <v-flex xs12 md6>
      <h1> <small>{{ $t('noums.evaluation') }} | </small> {{ project.name }}</h1>
    </v-flex>

    <template v-if="isUserProjectManager">
      <v-flex xs6 md3>
        <v-btn block :disabled="!bulletChartRoles" color="primary" class="elevation-0" @click="bulletChartRoles=false;createGraphs()">
          View Dimensions
        </v-btn>
      </v-flex>
      <v-flex xs6 md3>
        <v-btn block :disabled="bulletChartRoles" color="primary" class="elevation-0" @click="bulletChartRoles=true;createGraphs()">
          View by Role
        </v-btn>
      </v-flex>
    </template>

    <v-flex v-if="isUserProjectManager" xs12 class="text-xs-right">
      <v-btn flat outline color="black" :href="exportEvaluationURL">
        <v-icon>mdi-database-export</v-icon>
        {{ $t('actions.exportAllData') }}
      </v-btn>
    </v-flex>

    <v-flex xs12>
      <v-layout id="target-graph-area" row wrap>
        <!-- Overall Position -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('pages.evaluationDetail.projectOverallPosition') }}
                </h2>
                <HelpDialog
                  :title="$t('pages.evaluationDetail.projectOverallPosition')"
                  :text="$t('pages.evaluationDetail.help.projectOverallPosition')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text id="reference-width">
              <v-sheet height="200">
                <div id="scatterchart" />
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Project Evolution -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('pages.evaluationDetail.projectEvolution') }}
                </h2>
                <HelpDialog
                  :title="$t('pages.evaluationDetail.projectEvolution')"
                  :text="$t('pages.evaluationDetail.help.projectEvolution')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-sheet height="200">
                <div id="linechart" />
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-flex>

        <!--  Involvement -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('pages.evaluationDetail.heatchart.title') }}
                </h2>
                <HelpDialog
                  :title="$t('pages.evaluationDetail.heatchart.title')"
                  :text="$t('pages.evaluationDetail.help.involvement')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="heatchart" />
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- ================ -->
        <!-- PRINCIPLE CHARTS -->
        <!-- ================ -->

        <!-- Transform -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat style="background-color:#2F4193">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.transform') }}
                </h2>
                <HelpDialog
                  :title="$t('models.evaluation.principle.transform')"
                  :text="$t('pages.evaluationDetail.help.bulletChart.transformativeChange')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="transfchart" />
              <!-- Dimension Charts -->
              <div v-if="!bulletChartRoles" key="dimTransform">
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
              </div>
              <!-- Roles Charts -->
              <div v-else key="roleTransform">
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.projectManager') }}</h3>
                  <div id="TransformativeProjectChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.civilSociety') }}</h3>
                  <div id="TransformativeCivilChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.scientist') }}</h3>
                  <div id="TransformativeScientistChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.student') }}</h3>
                  <div id="TransformativeStudentChart" />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Knowledge -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat style="background-color:#2599D4">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.knowledge') }}
                </h2>
                <HelpDialog
                  color="white blue--text"
                  :title="$t('models.evaluation.principle.knowledge')"
                  :text="$t('pages.evaluationDetail.help.bulletChart.knowledgeDemocracy')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="knowchart" />
              <!-- Dimension Charts -->
              <div v-if="!bulletChartRoles" key="dimKnowledge">
                <div class="bullet">
                  <h3>{{ $t('models.evaluation.dimension.openness') }}</h3>
                  <div id="KnowledgeOpennessChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.evaluation.dimension.scientificRelevance') }}</h3>
                  <div id="KnowledgeRelevanceChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.evaluation.dimension.knowledgeIntegration') }}</h3>
                  <div id="KnowledgeTransdisciplChart" />
                </div>
              </div>
              <!-- Roles Charts -->
              <div v-else key="roleKnowledge">
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.projectManager') }}</h3>
                  <div id="KnowledgeProjectChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.civilSociety') }}</h3>
                  <div id="KnowledgeCivilChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.scientist') }}</h3>
                  <div id="KnowledgeScientistChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.student') }}</h3>
                  <div id="KnowledgeStudentChart" />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Participation -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="yellow darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.participation') }}
                </h2>
                <HelpDialog
                  color="white blue--text"
                  :title="$t('models.evaluation.principle.participation')"
                  :text="$t('pages.evaluationDetail.help.bulletChart.participatoryDynamics')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="partchart" />
              <!-- Dimension Charts -->
              <div v-if="!bulletChartRoles" key="dimParticipation">
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
              </div>
              <!-- Roles Charts -->
              <div v-else key="roleParticipation">
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.projectManager') }}</h3>
                  <div id="ParticipatoryProjectChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.civilSociety') }}</h3>
                  <div id="ParticipatoryCivilChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.scientist') }}</h3>
                  <div id="ParticipatoryScientistChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.student') }}</h3>
                  <div id="ParticipatoryStudentChart" />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Integrity -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="orange darken-3">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.integrity') }}
                </h2>
                <HelpDialog
                  color="white blue--text"
                  :title="$t('models.evaluation.principle.integrity')"
                  :text="$t('pages.evaluationDetail.help.bulletChart.integrity')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="integchart" />
              <!-- Dimension Charts -->
              <div v-if="!bulletChartRoles" key="dimIntegrity">
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
              </div>
              <!-- Roles Charts -->
              <div v-else key="roleIntegrity">
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.projectManager') }}</h3>
                  <div id="IntegrityProjectChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.civilSociety') }}</h3>
                  <div id="IntegrityCivilChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.scientist') }}</h3>
                  <div id="IntegrityScientistChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.student') }}</h3>
                  <div id="IntegrityStudentChart" />
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-flex>

        <!-- Citizen-Led -->
        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="teal darken-2">
              <v-toolbar-title>
                <h2 class="title">
                  {{ $t('models.evaluation.principle.citizen') }}
                </h2>
                <HelpDialog
                  color="white blue--text"
                  :title="$t('models.evaluation.principle.citizen')"
                  :text="$t('pages.evaluationDetail.help.bulletChart.citizenledResearch')"
                />
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <div id="citizchart" />
              <!-- Dimension Charts -->
              <div v-if="!bulletChartRoles" key="dimCitizen">
                <div class="bullet">
                  <h3>{{ $t('models.evaluation.dimension.communityAlignment') }}</h3>
                  <div id="CitizenCommunityChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.evaluation.dimension.responsivenessCommunityAlignment') }}</h3>
                  <div id="CitizenResponsivenessChart" />
                </div>
              </div>
              <!-- Roles Charts -->
              <div v-else key="roleCitizen">
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.projectManager') }}</h3>
                  <div id="CitizenProjectChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.civilSociety') }}</h3>
                  <div id="CitizenCivilChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.scientist') }}</h3>
                  <div id="CitizenScientistChart" />
                </div>
                <div class="bullet">
                  <h3>{{ $t('models.participationRole.student') }}</h3>
                  <div id="CitizenStudentChart" />
                </div>
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
import HelpDialog from "@/components/generic/HelpDialog";

import { createCommonGraphs, createParticipantBulletGraph, createManagerBulletGraph } from "@/plugins/vega.evaluation";
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
    EvaluationTextResponses,
    HelpDialog
  },

  data() {
    return {
      obj2slug,
      help: {
        overallPosition: false,
      },
      bulletChartRoles: false,
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
    },
    isUserProjectManager(){
      let userId = this.$store.getters['user/current'].id
      let project = this.$store.getters['project/detail'](this.projectId)

      // Check for all 3 posibilities
      let isManager = project.managers.indexOf(userId) != -1
      let isPM = project.participants.filter(p => p.role == 4).map(p => p.user).indexOf(userId) != -1
      let isOwner = project.owner == userId

      return isManager || isPM || isOwner
    },
    exportEvaluationURL(){
      return `${API_SERVER}/v1/csv/export/${this.projectId}/project_evaluation.csv`
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
      this.createGraphs()
    }, 300);

  },

  methods: {
    onResize(event){
      this.createGraphs()
    },

    createGraphs: debounce( function () {
      let width = document.querySelector("#reference-width").clientWidth
      createCommonGraphs(this.projectId, width)
      if(this.bulletChartRoles){
        createManagerBulletGraph(this.projectId, width)
      }else{
        createParticipantBulletGraph(this.projectId, width)
      }
    }, 100, {leading: false, trailing: true}),

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
  align-items: center;
  /* min-height: 68px; */
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
</style>
