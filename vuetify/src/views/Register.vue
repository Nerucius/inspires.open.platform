<style scoped>

  th, td{
    padding-bottom:10px
  }

</style>


<template>
  <v-layout align-content-start row wrap>
    <v-flex sm3 class="hidden-xs-only">
      <img height="150" src="/img/branding/inspires.png">
    </v-flex>

    <v-flex sm9 xs12>
      <h1 class="headline">Registration</h1>
      <p class="subheading">
        Welcome to the registration page for the InSPIRES Open Platform. Here you can create
        your own user to log into the site.
      </p>
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
                      :editable="isCompleted(idx+1)"
                    >
                      {{ step.title }}
                    </v-stepper-step>

                    <v-divider v-if="idx !== steps.length-1" :key="idx" />
                  </template>
                </v-stepper-header>

                <v-stepper-items>

                  <!-- Step 1 -->
                  <v-stepper-content step="1">
                    <v-sheet>
                      <v-layout row wrap justify-center>
                        <v-flex xs12>
                          <h2 class="title">First things first</h2>
                          <br>
                          <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis
                            debitis illum nulla magni tempora dolorem qui recusandae rerum
                            sed ipsam, dolorum nisi at aperiam laudantium distinctio itaque
                            delectus nesciunt ipsum.
                          </p>
                        </v-flex>
                        <v-flex xs12 sm8>
                          <v-form
                            ref="userPassForm"
                            v-model="steps[0].required.valid"
                          >
                            <v-text-field
                              v-model="user.username"
                              :label="$t('forms.fields.username')"
                              :hint="$t('forms.hints.username')"
                              :rules="[rules.required, rules.minimunLength6]"
                              prepend-icon="person"
                              type="text"
                            />
                            <v-text-field
                              v-model="user.password"
                              @input="$refs.userPassForm.validate()"
                              :label="$t('forms.fields.password')"
                              :hint="$t('forms.hints.password')"
                              :rules="[rules.required, rules.minimunLength, rules.passwordValid]"
                              prepend-icon="lock"
                              type="password"
                            />
                            <v-text-field
                              v-model="user.password2"
                              prepend-icon="lock"
                              :label="$t('forms.fields.passwordRepeat')"
                              :rules="[rules.passwordMatch]"
                              type="password"
                            />
                          </v-form>
                        </v-flex>
                      </v-layout>
                    </v-sheet>
                  </v-stepper-content>

                  <!-- Step 2 -->
                  <v-stepper-content step="2">
                    <v-sheet>
                      <v-layout row wrap justify-center>
                        <v-flex xs12>
                          <h2 class="title">Tell us a bit about yourself</h2>
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
                              v-model="user.first_name"
                              prepend-icon="person"
                              :label="$t('forms.fields.firstName')"
                              type="text"
                            />
                            <v-text-field
                              v-model="user.last_name"
                              prepend-icon="lock"
                              :label="$t('forms.fields.lastName')"
                            />
                            <v-text-field
                              v-model="user.email"
                              prepend-icon="lock"
                              :label="$t('forms.fields.email')"
                              type="email"
                              :rules="[rules.required, rules.isEmail]"
                            />
                          </v-form>
                        </v-flex>
                      </v-layout>
                    </v-sheet>
                  </v-stepper-content>

                  <!-- Step 3 -->
                  <v-stepper-content step="3">
                    <v-sheet min-height="300px">
                      <v-layout row wrap>
                        <v-flex xs12>
                          <h2 class="title">Terms of Service</h2>
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
                              :readonly="steps[2].required.acceptedTerms"
                              :depressed="steps[2].required.acceptedTerms"
                              :color="steps[2].required.acceptedTerms ? 'success' : 'primary'"
                              large
                              @click="steps[2].required.acceptedTerms=true"
                            >
                              <v-icon v-if="steps[2].required.acceptedTerms" left>
                                check
                              </v-icon>{{$t('pages.register.acceptTOS')}}
                            </v-btn>
                          </p>
                          <p v-if="steps[2].required.acceptedTerms">
                            Great! we can continue with the rest of the registration. Lorem
                            ipsum, dolor sit amet consectetur adipisicing elit. Necessitatibus
                            provident, hic ab molestias voluptates ducimus.
                          </p>
                        </v-flex>
                      </v-layout>
                    </v-sheet>
                  </v-stepper-content>

                  <!-- Step 4 -->
                  <v-stepper-content step="4">
                    <v-sheet min-height="300px">
                      <v-layout row wrap>
                        <v-flex xs12>
                          <h2 class="title">Review and Register</h2>
                          <br>
                          <p>
                            Please review the following information. If everything seems correct
                            you can proceed with registering.
                          </p>
                          <br>
                          <table width="100%">
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.username') }}:
                              </th>
                              <td class="text-xs-left pl-3">{{user.username || "Not specified"}}</td>
                            </tr>
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.firstName') }}:
                              </th>
                              <td class="text-xs-left pl-3">{{user.first_name || "Not specified"}}</td>
                            </tr>
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.lastName') }}:
                              </th>
                              <td class="text-xs-left pl-3">{{user.last_name || "Not specified"}}</td>
                            </tr>
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.email') }}:
                              </th>
                              <td class="text-xs-left pl-3">{{user.email || "Not specified"}}</td>
                            </tr>
                          </table>
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
              v-if="registrationStep != steps.length"
              color="primary"
              :disabled="!isCompleted(registrationStep)"
              @click="nextStep()"
            >
              {{ $t("actions.next") }}
            </v-btn>
            <v-btn
              v-else
              color="primary"
              @click="submitRegister()"
            >
              {{ $t("actions.register") }}
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
        { title: "Login", required: { valid: false } },
        { title: "About you", required: { valid: false } },
        { title: "ToS", required: { acceptedTerms: false } },
        { title: "Done!", required: { noedit:false } }
      ],

      user: {},
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minimunLength6: v => (v||"").length >= 6 || this.$t("forms.rules.minimunLength", {'length':6}),
        minimunLength: v => (v||"").length >= 8 || this.$t("forms.rules.minimunLength", {'length':8}),
        passwordValid: v => this.isValidPassword(v) || this.$t("forms.rules.passwordField"),
        passwordMatch: v => (this.user.password == this.user.password2) || this.$t("forms.rules.passwordMatch"),
        isEmail: v => this.isEmail(v) || this.$t("forms.rules.requiredField"),
      }
    };
  },

  methods: {

    async submitRegister(){
      let newUser = {...this.user}
      await this.$store.dispatch("user/register", newUser);

      this.$router.push("/account")
    },

    isEmail(value=""){
      let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(value).toLowerCase());
    },

    isValidPassword(value=""){
      value = value.toLowerCase()
      return true
        && value != "12345678"
        && value != "password"
        && value != "password1"
        && value != "password1234"
        && value != this.user.username
    },

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