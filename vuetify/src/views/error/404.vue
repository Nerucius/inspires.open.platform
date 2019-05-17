<template>
  <v-layout align-center justify-center>
    <v-flex xs12 sm8>
      <v-card>
        <v-toolbar dark class="elevation-0" color="error">
          <v-toolbar-title>
            <v-icon left>
              warning
            </v-icon>
            {{ $t('errors.404.title') }}
          </v-toolbar-title>
        </v-toolbar>


        <v-card-text class="py-5 px-5">
          <p class="headline">
            {{ $t('errors.404.text', {route: this.$route.path}) }}
          </p>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default{

    metaInfo(){
    return {
      title: this.$t('errors.404.title')
    }
  },

}

</script>