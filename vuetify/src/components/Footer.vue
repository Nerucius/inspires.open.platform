<template>
  <v-card flat>
    <v-card-text>
      <h1 class="subheading">
        InSPIRES Platform
      </h1>

      <v-layout row>
        <v-flex xs4>
          <br>

          <p>
          <router-link :to="{name:'terms-of-service'}">
            {{ $t('pages.termsOfService.mainTitle') }}
          </router-link>
          <br>
          <router-link :to="{name:'about'}">
            {{ $t('pages.about.mainTitle') }}
          </router-link>
          </p>
        </v-flex>

        <v-spacer />

        <v-flex xs4>
          <p>
            &copy; ISGlobal, Private Foundation {{ currentYear }}
          </p>
          <p>
            <small>
              <a href="https://cordis.europa.eu/project/rcn/106759/brief/en">
              <!-- <v-img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Flag_of_Europe.svg/1280px-Flag_of_Europe.svg.png"
                height="30" width="40" /> -->
                {{ $t('pages.footer.europeanFundingDisclaimer') }}
              </a>
            </small>
          </p>
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