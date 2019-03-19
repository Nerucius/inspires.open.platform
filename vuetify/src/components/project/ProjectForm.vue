<template>
  <v-form ref="form" v-model="valid">
    <h2>Project Details</h2>
    <p />

    <p class="subheading">
      Define your project information.
    </p>

    <v-text-field
      v-model="editedProject.acronym"
      box
      :rules="[rules.required]"
      counter="10"
      maxlength="10"
      label="Project Acronym"
      hint="Choose a Project Acronim."
    />
    <v-text-field
      v-model="editedProject.name"
      box
      :rules="[rules.required]"
      counter="50"
      label="Project Name"
      hint="Choose a name that characterizes your project.
                Less than 50 characters suggested."
    />
    <v-textarea
      v-model="editedProject.summary"
      box
      counter="200"
      label="Project Summary"
      hint="A short summary of your project and what it encompasses.
                Suggested to keep it under 200 characters."
    />

    <h2>Participants and Managers</h2>
    <p />
    <p class="subheading">
      People involved in the project.
    </p>

    <v-layout row wrap>
      <!-- Managers -->
      <v-flex sm12 md6>
        <v-combobox ref="managersCB"
                    v-model="editedProject.managers"
                    box
                    :items="userSearch"
                    :rules="[rules.isUser]"
                    label="Project Managers"
                    item-text="full_name"
                    item-value="id"
                    multiple
                    chips
                    deletable-chips
                    @update:searchInput="updateUserSearch($event)"
                    @input="clearSearch('managersCB')"
        />
      </v-flex>

      <!-- Participants -->
      <v-flex sm12 md6>
        <v-combobox ref="participantsCB"
                    v-model="editedProject.participants"
                    box
                    :items="userSearch"
                    :rules="[rules.isUser]"
                    label="Project Participants"
                    item-text="full_name"
                    item-value="id"
                    multiple
                    chips
                    deletable-chips
                    @update:searchInput="updateUserSearch($event)"
                    @input="clearSearch('participantsCB')"
        >
          <template v-slot:selection="data">
            <v-card class="mt-2 mb-3" style="width:100%">
              <v-card-text style="margin: -20px 0">
                <v-layout row justify-center align-center>
                  <v-flex pa-0>
                    <v-btn small icon color="error" outline
                           @click="removeParticipant(data.item)"
                    >
                      <v-icon small>
                        remove
                      </v-icon>
                    </v-btn>
                  </v-flex>
                  <v-flex xs6 py-0 px-2>
                    {{ data.item.full_name }}
                  </v-flex>
                  <v-flex xs6 py-0 px-1>
                    <v-select
                      v-model="data.item.role"
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
          </template>
        </v-combobox>
      </v-flex>
    </v-layout>


    <v-btn block large color="success"
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
  props: ["processing", "projectId"],

  data() {
    return {
      valid: null,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        isUser: v => this.isUser(v) || this.$t("forms.rules.mustBeUser"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
      userSearch: [],
      editedProject: {
        name: "",
        summary: "",
        participants: [],
        managers: [],
      },
      roles: [
        {id:1, name:"Scientist"},
        {id:2, name:"Student"},
        {id:3, name:"Civil Society"},
      ],
    };
  },

  async mounted() {
    this.$store.dispatch("structure/load");

    if (this.projectId) {
      // Editing existing project
      this.editedProject = this.loadProject(this.projectId)

    }else{
      // New Project
      this.editedProject.managers = [
        this.$store.getters["user/current"]
      ];
    }

    // Initialize user search with all visible users
    // this.userSearch = [...this.editedProject.participants, ...this.editedProject.managers]
  },

  methods: {
    user(uid){
      return this.$store.getters['user/get'](uid)
    },

    loadProject: async function(project){
      await this.$store.dispatch("project/load", [this.projectId]);
      let originalProject = this.$store.getters["project/detail"](
        this.projectId
      );

      // Transform attributes to be compatible with Form
      this.editedProject = { ...this.editedProject, ...originalProject };
      this.editedProject.managers = this.editedProject.managers.map(id => this.user(id))
      this.editedProject.participants = this.editedProject.participants.map(part =>
        ({...this.user(part.user), role: part.role, partId: part.id})
      )
    },

    removeParticipant(user){
      if(confirm(this.$t('dialog.confirm.participationDeletion'))){
        if(user.partId){
          this.$store.dispatch("participation/delete", user.partId)
        }

        this.editedProject.participants = this.editedProject.participants.filter(u => u.id != user.id)
      }
    },

    attemptSubmit: async function() {
      if (this.$refs.form.validate()) {
        let project = { ...this.editedProject };

        project.managers = project.managers.map(u => u.id)

        // De-transform the participation users back into participation objects
        project.participants = project.participants.map(user => (
          {
            id: user.partId,
            user: user.id,
            role: user.role,
            project: this.projectId,
          }
        ))

        await (Promise.all(
          project.participants.map(async part => {
            if(part.id){
              // Update
              await this.$store.dispatch("participation/update", part)
            }else{
              // Create
              await this.$store.dispatch("participation/create", part)
            }
          })
        ))

        if(this.projectId){
          await this.loadProject(this.projectId)
        }

        this.$emit("submit", project);
      }
    },

    isUser(value){
      // Check that all object are user instances
      if (!value) return true
      return !value.map(item => item.id == undefined).some(v => !!v)
    },

    clearSearch(ref) {
      this.$refs[ref].lazySearch = "";
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