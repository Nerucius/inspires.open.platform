<template>
  <v-layout align-content-start row wrap>
    <v-flex sm3 class="hidden-xs-only">
      <img height="150" src="/img/branding/inspires.png">
    </v-flex>

    <v-flex sm9 xs12>
      <h2>Registration</h2>
      <p class="subheading">
        Welcome to the registration page for the InSPIRES Open Platform. Here you can create
        your own user to log into the site.
      </p>
      <h3>Why Register?</h3>
      <p class="subheading">
        Registering allows you to start contributing to the site! You can also register Intermediation
        Organizations and Research Projects to your or your Organization's name.
      </p>
    </v-flex>

    <v-flex xs12 mt-3>
      <v-card class="elevation-12">
        <v-card-text class="pa-0">
          <v-layout row wrap>
            <!-- Form -->
            <v-flex pt-0>
              <v-stepper v-model="registrationStep" class="elevation-0 ma-0">
                <v-stepper-header>
                  <template v-for="(step, idx) in steps">
                    <v-stepper-step
                      :key="`${idx}-step`"
                      :complete="registrationStep > idx"
                      :step="idx+1"
                      editable
                    >
                      {{ step.title }}
                    </v-stepper-step>

                    <v-divider v-if="idx !== steps.length-1" :key="idx" />
                  </template>
                </v-stepper-header>

                <v-stepper-items>
                  <!-- Step 1 -->
                  <v-stepper-content step="1">
                    <v-sheet height="300px">
                      <v-layout row wrap>
                        <v-flex xs12>
                          <h3>Prequisites for Registering</h3>
                          <p />
                          <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis
                            debitis illum nulla magni tempora dolorem qui recusandae rerum
                            sed ipsam, dolorum nisi at aperiam laudantium distinctio itaque
                            delectus nesciunt ipsum.
                            <router-link to="/terms">
                              Terms of service
                            </router-link>
                          </p>
                          <p class="text-xs-center my-5">
                            <v-btn
                              :readonly="steps[0].required.acceptedTerms"
                              :depressed="steps[0].required.acceptedTerms"
                              :color="steps[0].required.acceptedTerms ? 'success' : 'primary'"
                              large
                              @click="steps[0].required.acceptedTerms=true"
                            >
                              <v-icon v-if="steps[0].required.acceptedTerms" left>
                                check
                              </v-icon>I Accept the Terms of Service
                            </v-btn>
                          </p>
                          <p v-if="steps[0].required.acceptedTerms">
                            Great! we can continue with the rest of the registration. Lorem
                            ipsum, dolor sit amet consectetur adipisicing elit. Necessitatibus
                            provident, hic ab molestias voluptates ducimus.
                          </p>
                        </v-flex>
                      </v-layout>
                    </v-sheet>
                  </v-stepper-content>

                  <!-- Step 2 -->
                  <v-stepper-content step="2">
                    <v-sheet>
                      <v-layout row wrap justify-center>
                        <v-flex xs12>
                          <h3>Your Login Details</h3>
                          <p />
                          <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis
                            debitis illum nulla magni tempora dolorem qui recusandae rerum
                            sed ipsam, dolorum nisi at aperiam laudantium distinctio itaque
                            delectus nesciunt ipsum.
                          </p>
                        </v-flex>
                        <v-flex xs12 sm8>
                          <v-form
                            v-model="steps[1].required.valid"
                          >
                            <v-text-field
                              v-model="user.username"
                              prepend-icon="person"
                              :label="$t('forms.fields.username')"
                              :rules="rules.required"
                              type="text"
                            />
                            <v-text-field
                              v-model="user.password"
                              prepend-icon="lock"
                              :label="$t('forms.fields.password')"
                              :rules="rules.password"
                              type="password"
                            />
                            <v-text-field
                              v-model="user.password2"
                              prepend-icon="lock"
                              :label="$t('forms.fields.passwordRepeat')"
                              :rules="rules.passwordMatch"
                              type="password"
                            />
                          </v-form>
                        </v-flex>
                      </v-layout>
                    </v-sheet>
                  </v-stepper-content>
                </v-stepper-items>
              </v-stepper>
            </v-flex>
          </v-layout>
        </v-card-text>

        <v-card-actions class="mt-2 pb-3 px-3">
          <v-spacer />
          <v-flex shrink>
            <v-btn
              v-if="registrationStep == steps.length"
              :disabled="!valid"
              color="primary"
              @click="submitLogin()"
            >
              {{ $t("actions.register") }}
            </v-btn>
            <v-btn
              v-else
              color="primary"
              :disabled="!isCompleted(registrationStep)"
              @click="nextStep()"
            >
              {{ $t("actions.next") }}
            </v-btn>
          </v-flex>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default {

  metaInfo: {
    title: "Register"
  },

  data() {
    return {
      registrationStep: 1,
      steps: [
        { title: "Welcome", required: { acceptedTerms: false } },
        { title: "Login", required: { valid: false } },
        { title: "Personal", required: { valid: false } },
        { title: "Done!", required: {} }
      ],

      user: {},
      rules: {
        required: [v => !!v || this.$t("forms.rules.requiredField")],
        password: [v => !!v || this.$t("forms.rules.requiredField")],
        passwordMatch: [v => (this.user.password == this.user.password2) || this.$t("forms.rules.passwordMatch")],
      }
    };
  },

  methods: {
    isCompleted(stepIdx) {
      let required = this.steps[stepIdx - 1].required;
      required = Object.values(required);
      return required == [] || required.every(v => !!v);
    },
    nextStep() {
      this.registrationStep = Math.min(
        this.steps.length,
        this.registrationStep + 1
      );
    }
  }
};
</script>