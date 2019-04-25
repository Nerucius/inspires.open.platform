<template>
  <v-card flat>
    <v-card-text>
      <h1 class="subheading">
        InSPIRES Platform
      </h1>

      <v-layout row>
        <v-flex xs4>
          <router-link :to="{name:'terms-of-service'}">
            Terms of Service
          </router-link>
          <br>
        </v-flex>

        <v-spacer />

        <v-flex xs4>
          &copy; ISGlobal, Private Foundation {{ currentYear }}
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data(){
    return{
      currentYear : new Date().getFullYear()
    }
  }
}
</script>