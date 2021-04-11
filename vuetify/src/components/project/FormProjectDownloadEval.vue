<template>
  <!-- Questionnaire download tool -->
  <div>

  <h2 class="my-4">{{ $t('pages.projectManage.evalViewPrintVersion') }}</h2>
  <v-card>
    <v-card-text>
      <v-form ref="form" v-model="valid" @submit.prevent="downloadQuestionnaire">
        <v-layout wrap>
          <v-flex xs12 sm6 md4>
            <v-select
              v-model="phase"
              :rules="[rules.required]"
              :items="Object.values(phases)"
              item-value="id"
              :item-text="tName"
              :label="$t('forms.fields.projectPhase')"
            />
          </v-flex>
          <v-flex xs12 sm6 md4>
            <v-select
              v-model="role"
              :rules="[rules.required]"
              :items="Object.values(roles)"
              item-value="id"
              :item-text="tName"
              :label="$t('forms.fields.role')"
            />
          </v-flex>
          <v-flex xs12 sm12 md4>
            <v-btn block dark color="red" type="submit">
              <v-icon left>print</v-icon>
              {{ $t("actions.viewAndPrint") }}
            </v-btn>
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
  </div>
</template>

<script>
export default {
  props: ["project"],

  data(){
    return {
      valid: null,
      phase: null,
      role: null,
      rules: {
        required: v => v!=undefined || this.$t("forms.rules.requiredField"),
      },
    }
  },

  computed: {
    phases() {
      return this.$store.getters["evaluation/phases"];
    },
    roles() {
      return this.$store.getters["evaluation/roles"];
    },
  },

  methods: {
    tName(obj) {
      return this.$t(obj.name);
    },

    async downloadQuestionnaire(){
      if(this.$refs.form.validate()){
        let evalQuestRoute = this.$router.resolve(
          { name:'evaluation-print',
            query: {
              project: this.project.id,
              version: this.project.eval_version,
              role:this.role,
              phase:this.phase
            }
          }
        ).route.fullPath;

        window.open(evalQuestRoute)
      }
    }
  },
};
</script>
