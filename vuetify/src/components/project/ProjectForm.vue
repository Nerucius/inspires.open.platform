<template>
  <v-form ref="form" v-model="valid">
    <h2>Project Details</h2>
    <p />
    <p class="subheading">
      Define the characteristics of your project
    </p>
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

    <h2>Researchers and Managers</h2>
    <p />
    <p class="subheading">
      People involved in the project
    </p>

    <v-combobox
      ref="researchersCB"
      v-model="editedProject.researcherUsernames"
      box
      :items="userSearch"
      label="Project Researchers"
      hint="Search by username all people involved in this project."
      chips
      multiple
      no-filter
      clearable
      @update:searchInput="updateUserSearch($event)"
      @input="clearSearch('researchersCB')"
    >
      <template v-slot:selection="data">
        <v-chip
          close
          class="subheading"
          :selected="data.selected"
          @input="removeResearcher(data.item)"
        >
          {{ data.item }}
        </v-chip>
      </template>
    </v-combobox>

    <v-combobox
      ref="managersCB"
      v-model="editedProject.managerUsernames"
      box
      :items="userSearch"
      label="Project Managers"
      hint="Search by username all people who should be able to manage the project."
      chips
      multiple
      no-filter
      clearable
      @update:searchInput="updateUserSearch($event)"
      @input="clearSearch('managersCB')"
    >
      <template v-slot:selection="data">
        <v-chip
          close
          class="subheading"
          :selected="data.selected"
          @input="removeManager(data.item)"
        >
          {{ data.item }}
        </v-chip>
      </template>
    </v-combobox>

    <v-btn block large color="success"
      :disabled="!valid || processing"
      :loading="processing"
      @click="attemptSubmit()">
      {{$t('actions.save')}}
    </v-btn>
  </v-form>
</template>


<script>
export default {
  props: ["processing", "projectId"],

  data() {
    return {
      valid: null,
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
      userSearch: [],
      editedProject: {
        name: "",
        summary: "",
        researchers: [],
        researcherUsernames: [],
        managers: [],
        managerUsernames: []
      }
    };
  },

  computed: {
    structures() {
      return this.$store.getters["structure/all"].map(s => s.name);
    }
  },

  async mounted() {
    this.$store.dispatch("structure/load");


    if (this.projectId != null) {
      await this.$store.dispatch("project/load", [this.projectId]);
      let originalProject = this.$store.getters["project/detail"](
        this.projectId
      );
      this.editedProject = { ...this.editedProject, ...originalProject };
      this.editedProject.managerUsernames = this.mapIdsToUsernames(this.editedProject.managers)
      this.editedProject.researcherUsernames = this.mapIdsToUsernames(this.editedProject.researchers)
    }else{
      this.editedProject.managerUsernames = [
        this.$store.getters["user/current"].username
      ];
    }
  },

  methods: {
    attemptSubmit() {
      if (this.$refs.form.validate()) {
        let project = { ...this.editedProject };

        project.managers = this.mapUsernamesToIds(project.managerUsernames);
        project.researchers = this.mapUsernamesToIds(
          project.researcherUsernames
        );
        delete project.managerUsernames;
        delete project.researcherUsernames;
        this.$emit("submit", project);
      }
    },

    mapUsernamesToIds(usernames) {
      let users = this.$store.getters["user/all"];
      return usernames.map(un => users.filter(u => u.username == un)[0].id);
    },

    mapIdsToUsernames(ids) {
      return ids.map(id => this.$store.getters["user/get"](id).username);
    },

    clearSearch(ref) {
      this.$refs[ref].lazySearch = "";
    },

    removeResearcher(username) {
      let usernames = this.project.researcherUsernames;
      usernames.splice(usernames.indexOf(username), 1);
      this.project.researcherUsernames = [...usernames];
    },

    removeManager(username) {
      let usernames = this.project.managerUsernames;
      usernames.splice(usernames.indexOf(username), 1);
      this.project.managerUsernames = [...usernames];
    },

    updateUserSearch(term) {
      term = term || "";
      if (term.length < 2) {
        this.userSearch = [];
        return;
      }
      term = new RegExp(term, "g");
      this.userSearch = this.$store.getters["user/all"]
        .map(u => u.username)
        .filter(u => u.match(term))
        .slice(0, 5);
    }
  }
};
</script>