<template>
  <v-form v-if="participants" ref="form" v-model="valid">
    <h2 class="mb-2">
      {{ $t('pages.projectManage.participantsTitle') }}
    </h2>

    <v-alert color="info" class="ma-4" :value="true" dismissible>
      <v-layout row align-top>
        <v-flex shrink>
          <v-icon large dark>
            info
          </v-icon>
        </v-flex>
        <v-flex>
          <vue-markdown>{{ $t('pages.projectManage.participantsIntro') }}</vue-markdown>
        </v-flex>
      </v-layout>
    </v-alert>

    <v-form ref="form" v-model="valid">
      <p class="pa-2 grey lighten-3">
        <v-card v-for="item in participants" :key="item.id"
                class="ma-1 mb-3"
        >
          <v-card-text>
            <v-layout row justify-center align-center>
              <v-flex pa-0>
                <v-btn small icon color="error" outline
                       @click="removeParticipant(item)"
                >
                  <v-icon small>
                    remove
                  </v-icon>
                </v-btn>
              </v-flex>
              <v-flex xs6 py-0 px-2>
                {{ item.full_name }}
              </v-flex>
              <v-flex xs6 py-0 px-1>
                <v-select
                  v-model="item.role"
                  :label="$t('forms.fields.role')"
                  :rules="[rules.required]"
                  :items="Object.values(roles)"
                  :item-text="tName"
                  item-value="id"
                />
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </p>
    </v-form>

    <v-combobox v-model="targetUser"
                box
                :label="$t('forms.labels.searchUsers')"
                :items="userSearch"
                item-text="form_name"
                item-value="id"
                @update:searchInput="updateUserSearch($event)"
                @change="addParticipant($event); clearSearch()"
    />

    <v-btn block large
           color="success"
           :disabled="!valid || processing"
           :loading="processing"
           @click="attemptSubmit()"
    >
      {{ $t('actions.save') }}
    </v-btn>
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
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
      participants: null,
      processing: false,
      userSearch: [],
      targetUser: null
    };
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"]
    },
    roles(){
      return this.$store.getters['evaluation/roles']
    },
  },

  async mounted() {
    this.loadParticipants()

    let listener = this.$root.$on('project-manage:invite', () => {
      this.loadParticipants()
    })
  },


  destroyed() {
    // cancel all subs
    this.$root.$off('project-manage:invite')
  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
    },

    tName(obj){
      return this.$t(obj.name)
    },


    loadParticipants: async function(){
      // Transform attributes to be compatible with Form
      this.participants = this.project.participants.map(part =>
        ({
          ...this.user(part.user),
          role: part.role,
          partId: part.id
        })
      )
    },

    attemptSubmit: async function() {
      if (this.$refs.form.validate()) {

        // De-transform the participation users back into participation objects
        let participants = this.participants.map(user => (
          {
            id: user.partId,
            user: user.id,
            role: user.role,
            project: this.project.id,
          }
        ))

        try{
          await (Promise.all(
            participants.map(async part => {
              if(part.id){
                // Update
                await this.$store.dispatch("participation/update", part)
              }else{
                // Create
                await this.$store.dispatch("participation/create", part)
              }
            })
          ))

          this.$store.dispatch("toast/success", this.$t('forms.toasts.saveSuccess'))
          await this.$store.dispatch("project/load",[this.project.id])
          this.loadParticipants()

        }catch(error){
          this.$store.dispatch("toast/error", {
            message:this.$t('forms.toasts.saveFailure'),
            error
          })
        }

      }
    },

    isUser(value){
      // Check that all object are user instances
      if (!value) return true
      return !value.map(item => item.id == undefined).some(v => !!v)
    },

    addParticipant(user){
      if(!!user.id && this.participants.filter(p => p.id == user.id).length == 0){
        this.participants = [...this.participants, user]
      }
    },

    removeParticipant: async function(user){
      if( confirm(this.$t('dialog.confirm.participationDeletion')) ) {
        // Delete only if participation was saved
        if(!!user.partId){
          try{
            await this.$store.dispatch("participation/delete", user.partId)
            this.$store.dispatch("toast/success", this.$t('forms.toasts.saveSuccess'))
          }catch(error){
            this.$store.dispatch("toast/error", {error, message:this.$t('forms.toasts.saveFailure')})
          }
        }

        this.participants = this.participants.filter(u => u.id != user.id)
      }

      await this.$store.dispatch("project/load",[this.project.id])
      this.loadParticipants()
    },

    clearSearch() {
      this.$nextTick(() => {
        this.targetUser = null
      })
    },


    updateUserSearch(term) {
      term = term || "";
      if (term.length < 2) {
        this.userSearch = [];
        return;
      }
      term = new RegExp(term, "gi");
      this.userSearch = cloneDeep(
        this.$store.getters["user/all"]
        .filter(u => u.username.match(term) || u.full_name.match(term))
        .slice(0, 5)
      )
    }

  }
};
</script>
