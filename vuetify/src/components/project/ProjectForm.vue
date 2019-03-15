<template>
  <v-form ref="form" v-model="valid">
    <h2>Project Details</h2>
    <p />
    <p class="subheading">
      Define the characteristics of your project.
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
      People involved in the project.
    </p>

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

    <v-combobox ref="researchersCB"
                v-model="editedProject.researchers"
                box
                :items="userSearch"
                :rules="[rules.isUser]"
                label="Project Researchers"
                item-text="full_name"
                item-value="id"
                multiple
                chips
                deletable-chips
                @update:searchInput="updateUserSearch($event)"
                @input="clearSearch('researchersCB')"
    />

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
        researchers: [],
        managers: [],
      }
    };
  },

  async mounted() {
    let store = this.$store

    store.dispatch("structure/load");

    if (this.projectId != null) {
      // Editing existing project
      await store.dispatch("project/load", [this.projectId]);
      let originalProject = store.getters["project/detail"](
        this.projectId
      );
      this.editedProject = { ...this.editedProject, ...originalProject };
      this.editedProject.researchers = this.editedProject.researchers.map(id => store.getters['user/get'](id))
      this.editedProject.managers = this.editedProject.managers.map(id => store.getters['user/get'](id))

    }else{
      // New Project
      this.editedProject.managers = [
        this.$store.getters["user/current"]
      ];
    }

    // Initialize user search with all visible users
    this.userSearch = [...this.editedProject.researchers, ...this.editedProject.managers]
  },

  methods: {
    attemptSubmit() {
      if (this.$refs.form.validate()) {
        let project = { ...this.editedProject };
        project.managers = project.managers.map(u => u.id)
        project.researchers = project.researchers.map(u => u.id)
        this.$emit("submit", project);
      }
    },

    isUser(value){
      // Check that all object are user instances
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
      this.userSearch = this.$store.getters["user/all"]
        .filter(u => u.username.match(term))
        .slice(0, 5);
    }
  }
};
</script>