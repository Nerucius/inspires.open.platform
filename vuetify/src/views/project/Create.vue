<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <h1>Create new Project</h1>
    </v-flex>

    <v-flex xs12 mb-5>
      <v-card flat>
        <v-card-text>
          <v-form v-model="valid">
            <h2>Project Details</h2>
            <p></p>
            <p class="subheading">Define the characteristics of your project</p>
            <v-text-field
              box
              counter="50"
              v-model="project.name"
              label="Project Name"
              hint="Choose a name that characterizes your project.
                Less than 50 characters suggested."
            />
            <v-textarea
              box
              counter="200"
              v-model="project.summary"
              label="Project Summary"
              hint="A short summary of your project and what it encompasses.
                Suggested to keep it under 200 characters."
            />

            <h2>Researchers and Managers</h2>
            <p></p>
            <p class="subheading">People involved in the project</p>

            <v-combobox box ref="researchersCB"
              v-model="project.researcherUsernames"
              @update:searchInput="updateUserSearch($event)"
              @input="clearSearch('researchersCB')"
              :items="userSearch"
              label="Project Researchers"
              hint="Search by username all people involved in this project."
              chips
              multiple
              no-filter
              clearable
              >
              <template v-slot:selection="data">
                <v-chip close
                  class="subheading"
                  :selected="data.selected"
                  @input="removeResearcher(data.item)"
                >
                  {{ data.item }}
                </v-chip>
              </template>
            </v-combobox>

            <v-combobox box ref="managersCB"
              v-model="project.managerUsernames"
              @update:searchInput="updateUserSearch($event)"
              @input="clearSearch('managersCB')"
              :items="userSearch"
              label="Project Managers"
              hint="Search by username all people who should be able to manage the project."
              chips
              multiple
              no-filter
              clearable
              >
              <template v-slot:selection="data">
                <v-chip close
                  class="subheading"
                  :selected="data.selected"
                  @input="removeManager(data.item)"
                >
                  {{ data.item }}
                </v-chip>
              </template>
            </v-combobox>

            <h2>Your Intermediation Structure</h2>
            <p></p>

            <v-select
              v-model="collaboration.structure"
              :items="structures"
              box
              >

            </v-select>

          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>

  </v-layout>
</template>

<script>
import ProjectCard from "@/components/project/ProjectCard";

export default {
  components: {
    ProjectCard
  },

  data() {
    return {
      valid: null,
      userSearch:[],
      collaboration:{
        structure:null,
      },
      project: {
        id: "0",
        name: "",
        summary: "",
        researchers: [],
        researcherUsernames: [],
        managers: [],
        managerUsernames: [],
        rating: 4
      },
    };
  },

  mounted(){
    this.$store.dispatch("structure/load")
  },

  methods:{
    clearSearch(ref){
      this.$refs[ref].lazySearch = ""
    },

    removeResearcher(username){
      let usernames = this.project.researcherUsernames
      usernames.splice(usernames.indexOf(username), 1)
      this.project.researcherUsernames = [...usernames]
    },

    removeManager(username){
      let usernames = this.project.managerUsernames
      usernames.splice(usernames.indexOf(username), 1)
      this.project.managerUsernames = [...usernames]
    },

    updateUserSearch(term){
      term = term || ""
      if (term.length < 2){
        this.userSearch = []
        return
      }
      term = new RegExp(term, 'g')
      this.userSearch = this.$store.getters['user/all']
        .map(u => u.username)
        .filter(u => u.match(term))
        .slice(0,5)
    }
  },


  computed:{
    structures(){
      return this.$store.getters['structure/all'].map(s => s.name)
    }
  },
};
</script>
