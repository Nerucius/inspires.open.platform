<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex xs12>
      <h1>Evaluation for {{ project.name }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-card flat>
        <v-card-text id="target-graph-area">
          <!-- MIREIA CODE FOR EVALUATION -->

          <div id="main">
            <div id="scatter">
              <h2 style="width:100%">
                Project Overall Position
              </h2>
              <hr style="border: 2px solid gray">
              <div id="scatterchart" />
            </div>
            <div id="line">
              <h2>Project Evolution</h2>
              <hr style="border: 2px solid gray">
              <div id="linechart" />
            </div>
            <div id="transf">
              <h2>Transformative Change</h2>
              <hr style="border: 2px solid #2F4193">
              <div id="transfchart" />
              <div class="bullet">
                <h3>Collective capacity</h3>
                <div id="TransformativeCollectiveChart" />
              </div>
              <div class="bullet">
                <h3>Knowledge and skills</h3>
                <div id="TransformativeSkillsChart" />
              </div>
              <div class="bullet">
                <h3>Policy impact</h3>
                <div id="TransformativePolicyChart" />
              </div>
              <div class="bullet">
                <h3>Self-improvement</h3>
                <div id="TransformativeSelfChart" />
              </div>
              <div id="partic">
                <h2>Participatory Dynamics</h2>
                <hr style="border: 2px solid #DAE14B">
                <div id="partchart" />
                <div class="bullet">
                  <h3>Degree of engagement</h3>
                  <div id="ParticipatoryEngagementChart" />
                </div>
                <div class="bullet">
                  <h3>Impact of the participatory dynamics</h3>
                  <div id="ParticipatoryImpactChart" />
                </div>
                <div class="bullet">
                  <h3>Motivation</h3>
                  <div id="ParticipatoryMotivationChart" />
                </div>
                <div class="bullet">
                  <h3>Satisfaction with the participatory dunamics</h3>
                  <div id="ParticipatorySatisfactionChart" />
                </div>
              </div>
              <div id="know">
                <h2>Knowledge Democracy</h2>
                <hr style="border: 2px solid #2599D4">
                <div id="knowchart" />
                <div class="bullet">
                  <h3>Openness</h3>
                  <div id="KnowledgeOpennessChart" />
                </div>
                <div class="bullet">
                  <h3>Scientific relevance</h3>
                  <div id="KnowledgeRelevanceChart" />
                </div>
                <div class="bullet">
                  <h3>Transdisciplinarity</h3>
                  <div id="KnowledgeTransdisciplChart" />
                </div>
              </div>
            </div>
            <div id="heat">
              <h2>Involvement</h2>
              <hr style="border: 2px solid gray">
              <div id="heatchart" />
              <div id="citiz">
                <h2>Citizen-led Research</h2>
                <hr style="border: 2px solid #00796B">
                <div id="citizchart" />
                <div class="bullet">
                  <h3>Community alignment</h3>
                  <div id="CitizenCommunityChart" />
                </div>
                <div class="bullet">
                  <h3>Responsiveness to community alignment</h3>
                  <div id="CitizenResponsivenessChart" />
                </div>
              </div>
              <div id="integ">
                <h2>Integrity</h2>
                <hr style="border: 2px solid #F17600">
                <div id="integchart" />
                <div class="bullet">
                  <h3>Expectation alignment</h3>
                  <div id="IntegrityExpectationChart" />
                </div>
                <div class="bullet">
                  <h3>Gender perspective</h3>
                  <div id="IntegrityGenderChart" />
                </div>
                <div class="bullet">
                  <h3>Inclusivity</h3>
                  <div id="IntegrityInclusivityChart" />
                </div>
                <div class="bullet">
                  <h3>Reflexivity</h3>
                  <div id="IntegrityReflexivityChart" />
                </div>
                <div class="bullet">
                  <h3>Resource availability</h3>
                  <div id="IntegrityResourceChart" />
                </div>
                <div class="bullet">
                  <h3>Transparency</h3>
                  <div id="IntegrityTransparencyChart" />
                </div>
              </div>
            </div>
          </div>

          <!-- /MIREIA CODE FOR EVALUATION -->
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { slug2id, obj2slug } from "@/plugins/utils";
import { setTimeout } from 'timers';

export default {
  metaInfo() {
    return {
      title: (this.project || {}).name
    };
  },

  data() {
    return {
      obj2slug,
      project: null,
      graphAreaWidth: undefined,
    };
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    structure() {
      return this.$store.getters["structure/detail"](
        this.project.collaboration.structure
      );
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
      this.$store.dispatch("project/load");
      await this.$store.dispatch("project/load", [this.projectId]);
      this.project = this.$store.getters["project/detail"](this.projectId);
      this.$store.dispatch("structure/load", [
        this.project.collaboration.structure
      ]);
    } catch (err) {
      // TODO: Show error instead
      this.$router.push("/project-not-found");
    }

    window.addEventListener("resize", this.onResize);

    setTimeout(() => {
      createParticipantGraph(`http://localhost:8080/v1/csv/eval/${this.projectId}`)
    }, 500);

  },

  updated(){
    console.log("updated")
    // createParticipantGraph(`http://localhost:8080/v1/csv/eval/${this.projectId}`)
  },

  methods: {
    onResize(event){
      // console.log(event)
      // let width = document.querySelector("#target-graph-area").clientWidth
      // console.log(width)
      // this.graphAreaWidth = width / 3
      // createParticipantGraph(`http://localhost:8080/v1/csv/eval/${this.projectId}`)
    },

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
hr {
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
}
</style>
