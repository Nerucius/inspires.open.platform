<template>
  <v-form v-if="participants" ref="form" v-model="valid">
    <h2>Participants in this Project</h2>
    <p />

    <p class="subheading">
      Add all the people helping to make this project possible here. Each person can
      have a role within the project. The Role will be used in determining what role
      they play in the impact evaluation tool.
    </p>

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
                  :items="roles"
                  item-text="name"
                  item-value="id"
                />
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </p>
    </v-form>

    <v-combobox
      v-model="targetUser"
      box
      label="Search Users"
      :items="userSearch"
      item-text="full_name"
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
      targetUser: null,
      roles: [
        {id:1, name:"Scientist"},
        {id:2, name:"Student"},
        {id:3, name:"Civil Society"},
      ],
    };
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"]
    }
  },

  async mounted() {
    this.loadParticipants()
  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
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

        this.loadParticipants()
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

    removeParticipant(user){
      console.log(user)

      if( confirm(this.$t('dialog.confirm.participationDeletion')) ) {
        // Delete only if participation was saved
        if(!!user.partId){
          this.$store.dispatch("participation/delete", user.partId)
        }

        this.participants = this.participants.filter(u => u.id != user.id)
      }
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