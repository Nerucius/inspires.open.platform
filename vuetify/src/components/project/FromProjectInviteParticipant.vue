<template>
  <v-form ref="form" v-model="valid">
    <h2 class="mb-2">
      {{ $t("pages.projectManage.inviteParticipantsTitle") }}
    </h2>

    <v-alert color="info" class="ma-4" :value="true" dismissible>
      <v-layout row align-top>
        <v-flex shrink>
          <v-icon large dark>info</v-icon>
        </v-flex>
        <v-flex>
          <vue-markdown>{{
              $t("pages.projectManage.inviteParticipantsInfo")
            }}</vue-markdown>
        </v-flex>
      </v-layout>
    </v-alert>

    <v-form ref="form" v-model="valid" @submit.prevent="attemptSubmit()">
      <v-card>
        <v-card-text>
          <h2>{{ $t("forms.titles.newParticipant") }}</h2>

          <v-select
            v-model="inviteUser.role"
            :items="roles"
            :label="$t('forms.fields.role')"
            :rules="[rules.required]"
            :item-text="translateName"
            item-value="id"
          />

          <v-checkbox
            v-model="inviteUser.hide_realname"
            :label="$t('forms.fields.isAnonymous')"
            :hint="$t('forms.hints.isAnonymousInvite')"
            persistent-hint
          />

          <v-layout wrap>
            <v-flex xs12 sm6>
              <v-text-field
                v-model="inviteUser.first_name"
                maxlength="255"
                :rules="[rules.required]"
                :label="$t('forms.fields.firstName')"
              />
            </v-flex>
            <v-flex xs12 sm6>
              <v-text-field
                v-model="inviteUser.last_name"
                maxlength="255"
                :rules="[rules.required]"
                :label="$t('forms.fields.lastName')"
              />
            </v-flex>
          </v-layout>

          <v-text-field
            v-model="inviteUser.email"
            :rules="[rules.isEmail]"
            :label="$t('forms.fields.email')"
            :hint="$t('misc.optional')"
            persistent-hint
          />
          <v-text-field
            v-model="inviteUser.institution"
            :label="$t('forms.fields.institution')"
            :hint="$t('misc.optional')"
            persistent-hint
          />
        </v-card-text>

        <v-card-actions>
          <v-btn
            type="submit"
            color="success"
            :disabled="!valid || processing"
            :loading="processing"
            large block
          >
            {{ $t("actions.invite") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-form>
</template>


<script>
import { cloneDeep } from "lodash";

export default {
  props: ["project"],

  data() {
    return {
      valid: null,
      rules: {
        required: (v) => !!v || this.$t("forms.rules.requiredField"),
        isEmail: (v) => this.isEmail(v) || this.$t("forms.rules.invalidEmail"),
      },
      inviteUser: {},
      processing: false,
    };
  },

  computed: {
    roles() {
      return Object.values(this.$store.getters["evaluation/roles"]);
    },
  },

  methods: {
    attemptSubmit: async function () {
      if (this.$refs.form.validate()) {
        try {
          await this.$store.dispatch("project/invite", {
            id: this.project.id,
            user: this.inviteUser,
          });

          this.$store.dispatch(
            "toast/success",
            this.$t("forms.toasts.inviteParticipantSuccess")
          );

          await this.$store.dispatch("user/load");
          await this.$store.dispatch("project/load", [this.project.id]);
          this.$root.$emit('project-manage:invite')

          this.inviteUser = {}
          this.$refs.form.reset()

        } catch (error) {
          this.$store.dispatch("toast/error", {
            message: this.$t("forms.toasts.inviteParticipantFailure"),
            error,
          });
        }
      }
    },

    isExistingUser() {},

    isEmail(value) {
      if(!value) return true;
      let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(value).toLowerCase());
    },

    translateName(item) {
      return this.$t(item.name);
    },

  },
};
</script>
