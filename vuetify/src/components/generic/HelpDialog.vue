<style scoped>
  .help__button{
    margin-top: 23px;
    margin-right:-12px;
    transform: scale(.75)
  }

  .help__button .v-icon{
    transform: scale(1.25)
  }
</style>

<template>
  <v-btn
    fab small dark :color="color || 'blue white--text'" absolute top right class="help__button elevation-0"
    @click="showHelp = true">
    <v-icon>mdi-help</v-icon>
    <!-- Dialog -->
    <v-dialog v-model="showHelp" max-width="600">
      <v-card>
        <v-toolbar dense dark flat color="primary">
          <v-toolbar-title>
            {{ title }}
          </v-toolbar-title>
        </v-toolbar>
        <v-card-text><vue-markdown>{{ text }}</vue-markdown></v-card-text>
      </v-card>
    </v-dialog>
  </v-btn>
</template>

<script>
export default {
  props: ['title', 'text', 'color'],

  data() {
    return {
      showHelp: false,
    }
  },
}
</script>
