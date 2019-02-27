<template>
  <v-menu full-width offset-y>
    <v-btn slot="activator" block flat>
      Theme: {{ $store.getters["preferences/theme"] }}
      <v-icon right>
        expand_more
      </v-icon>
    </v-btn>
    <v-list>
      <v-list-tile v-for="(theme, index) in themes" :key="index" @click="setTheme(theme)">
        <v-list-tile-action>
          <v-icon v-if="theme == $store.getters['preferences/theme']">
            check
          </v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <div class="text-xs-center">
            {{ theme | uppercase }}
          </div>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </v-menu>
</template>


<script>
export default {
  name: "LanguageSelector",

  data() {
    return {
      themes: ["dark", "light"]
    };
  },

  methods: {
    setTheme(theme) {
      this.$store.dispatch("preferences/set", { theme });
    }
  }
};
</script>
