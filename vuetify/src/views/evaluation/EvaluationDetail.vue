<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex xs12>
      <h1>Evaluation for {{ project.name }}</h1>
    </v-flex>

    <v-flex xs12>
      <v-layout id="target-graph-area" row wrap>


        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">Project Overall Position</h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text id="reference-width">
              <v-sheet height=200>
                <div id="scatterchart" />
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="grey darken-3">
              <v-toolbar-title>
                <h2 class="title">Project Evolution</h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-sheet height=200>
                <div id="linechart" />
              </v-sheet>
            </v-card-text>
          </v-card>
        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat style="background-color:#2F4193">
              <v-toolbar-title>
                <h2 class="title">Transformative Change</h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>
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
            </v-card-text>
          </v-card>


        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat style="background-color:#2599D4">
              <v-toolbar-title>
                <h2 class="title">Knowledge Democracy</h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>

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
            </v-card-text>
          </v-card>


        </v-flex>

        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="green darken-2">
              <v-toolbar-title>
                <h2 class="title">Participatory Dynamics</h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>

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
            </v-card-text>
          </v-card>

        </v-flex>


        <v-flex xs12 sm6 xl4>
          <v-card>
            <v-toolbar dense dark flat color="orange darken-3">
              <v-toolbar-title>
                <h2 class="title">Integrity</h2>
              </v-toolbar-title>
            </v-toolbar>
            <v-card-text>

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
            </v-card-text>
          </v-card>

        </v-flex>



      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import { createParticipantGraph } from "@/plugins/vega.evaluation";
import { slug2id, obj2slug } from "@/plugins/utils";
import { API_SERVER } from '@/plugins/resource';
import { debounce } from "lodash";

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
      this.createGraph()
    }, 300);

  },

  methods: {
    onResize(event){
      this.createGraph()
    },

    createGraph: debounce( function () {
      let width = document.querySelector("#reference-width").clientWidth
      createParticipantGraph(`http://localhost:8080/v1/csv/eval/${this.projectId}`, width)
    }),

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

.v-card__text{
  /* padding: 0px; */
  /* margin: 20px; */
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
