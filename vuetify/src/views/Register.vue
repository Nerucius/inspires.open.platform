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
      <h1 class="headline">
        {{ $t('actions.register') }}
      </h1>
      <p class="subheading">
        {{ $t('pages.register.welcomeMessage') }}
      </p>
      <p class="subheading hidden-xs-only">
        {{ $t('pages.register.welcomeMessage2') }}
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
                          <h2 class="title">
                            {{ $t('pages.register.titles.step1') }}
                          </h2>
                          <br>
                          <p>
                            {{ $t('pages.register.step1Message') }}
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
                              :label="$t('forms.fields.password')"
                              :hint="$t('forms.hints.password')"
                              :rules="[rules.required, rules.minimunLength, rules.passwordValid]"
                              prepend-icon="lock"
                              type="password"
                              @input="$refs.userPassForm.validate()"
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
                          <h2 class="title">
                            {{ $t('pages.register.titles.step2') }}
                          </h2>
                          <p />
                          <p>
                            {{ $t('pages.register.step2Message') }}
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
                              :rules="[rules.required]"
                              type="text"
                            />
                            <v-text-field
                              v-model="user.last_name"
                              prepend-icon="lock"
                              :label="$t('forms.fields.lastName')"
                              :rules="[rules.required]"
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

                  <!-- Step 3 - TOS -->
                  <v-stepper-content step="3">
                    <v-sheet min-height="300px">
                      <v-layout row wrap>
                        <v-flex xs12>
                          <h2 class="title mb-2">
                            {{ $t('pages.register.titles.step3') }}
                          </h2>
                          <p>
                            {{ $t('pages.register.step3Message') }}
                            <router-link target="_blank" :to="{name:'terms-of-service'}">
                              {{ $t('pages.register.readTOSHere') }}
                            </router-link>
                          </p>
                          <p>
                            {{ $t('pages.register.step3TOSAcceptance') }}
                          </p>
                          <p class="text-xs-center my-5">
                            <v-btn
                              large
                              class="px-2"
                              :readonly="steps[2].required.acceptedTerms"
                              :depressed="steps[2].required.acceptedTerms"
                              :color="steps[2].required.acceptedTerms ? 'success' : 'primary'"
                              @click="steps[2].required.acceptedTerms=true"
                            >
                              <v-icon v-if="steps[2].required.acceptedTerms">
                                check
                              </v-icon>&nbsp;{{ $t('pages.register.acceptTOS') }}
                            </v-btn>
                          </p>
                          <p v-if="steps[2].required.acceptedTerms">
                            {{ $t('pages.register.step3MessageAccepted') }}
                          </p>
                        </v-flex>
                      </v-layout>
                    </v-sheet>
                  </v-stepper-content>

                  <!-- Step 4 -->
                  <v-stepper-content step="4">
                    <v-sheet min-height="300px">
                      <v-layout row wrap justify-center>
                        <v-flex xs12>
                          <h2 class="title">
                            {{ $t('pages.register.titles.step4') }}
                          </h2>
                          <br>
                          <p>
                            {{ $t('pages.register.step4Message') }}
                          </p>
                          <table width="100%">
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.username') }}:
                              </th>
                              <td class="text-xs-left pl-3">
                                {{ user.username || "Not specified" }}
                              </td>
                            </tr>
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.firstName') }}:
                              </th>
                              <td class="text-xs-left pl-3">
                                {{ user.first_name || "Not specified" }}
                              </td>
                            </tr>
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.lastName') }}:
                              </th>
                              <td class="text-xs-left pl-3">
                                {{ user.last_name || "Not specified" }}
                              </td>
                            </tr>
                            <tr>
                              <th width="50%" class="text-xs-right pr-3">
                                {{ $t('forms.fields.email') }}:
                              </th>
                              <td class="text-xs-left pl-3">
                                {{ user.email || "Not specified" }}
                              </td>
                            </tr>
                          </table>
                        </v-flex>

                        <v-flex xs12>
                          <v-alert :value="failedRegistration">
                            <v-icon dark left>
                              warning
                            </v-icon>
                            The registration has failed. Your username might be in use.
                          </v-alert>
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
              :disabled="!isCompleted(registrationStep)"
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

  metaInfo(){
    return {
      title: this.$t("actions.register")
    }
  },

  data() {
    return {
      failedRegistration: false,
      registrationStep: 1,
      steps: [
        { title: "Login", required: { valid: false } },
        { title: "About you", required: { valid: false } },
        { title: "ToS", required: { acceptedTerms: false } },
        { title: "Done!", required: { valid:true } }
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

  mounted(){
    this.$store.dispatch("user/logout")
  },

  methods: {

    async submitRegister(){
      let newUser = {...this.user}
      try{
        let response = (await this.$store.dispatch("user/register", newUser))
        await this.$store.dispatch("user/load")
        await this.$store.dispatch("user/login", {
          username: newUser.username,
          password: newUser.password
        })
        this.$router.push({ name: 'account', query: { newUser: true } })

      } catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.register.registrationFailure"),
          error
        })
        this.failedRegistration = true
      }
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
        && value != "password12"
        && value != "password123"
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