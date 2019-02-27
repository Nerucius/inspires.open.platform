<template>
  <v-menu offset-y>
    <v-btn slot="activator" flat>
      {{ currentLanguage }}
      <v-icon right>
        expand_more
      </v-icon>
    </v-btn>
    <v-list>
      <v-list-tile
        v-for="(lang, index) in listOfLocales"
        :key="index"
        @click="selectLanguage(lang)"
      >
        <v-list-tile-title>
          <small>{{ lang | uppercase }}</small>
        </v-list-tile-title>

        <flag :iso="flag[lang]" :squared="false" style="width:40px" />
      </v-list-tile>
    </v-list>
  </v-menu>
</template>


<script>
import { listOfLocales } from "@/plugins/i18n";

export default {
  name: "LanguageSelector",

  data() {
    return {
      listOfLocales,
      flag: {
        en: "gb",
        es: "es",
        ca: "es-ct"
      }
    };
  },

  computed: {
    currentLanguage() {
      return this.$store.getters["preferences/lang"];
    }
  },

  methods: {
    selectLanguage(lang) {
      this.$store.dispatch("preferences/set", { lang });
    }
  }
};
</script>
