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
        v-for="(lang, index) in ListOfLocales"
        :key="index"
        @click="selectLanguage(lang)"
      >
        <v-list-tile-title>
          <small>{{ lang | uppercase }}</small>
        </v-list-tile-title>

        <flag :iso="getFlag(lang)" :squared="false" style="width:40px" />
      </v-list-tile>
    </v-list>
  </v-menu>
</template>


<script>
import { ListOfLocales } from "@/plugins/i18n";

export default {
  name: "LanguageSelector",

  data() {
    return {
      ListOfLocales,
    };
  },

  computed: {
    currentLanguage() {
      return this.$store.getters["preferences/lang"];
    }
  },

  methods: {
    getFlag(lang){
      if (lang == "en" ) return "gb"
      if (lang == "ca" ) return "es-ct"
      if (lang == "ar" ) return "tn"
      return lang
    },

    selectLanguage(lang) {
      // change text orientation
      this.$vuetify.rtl = lang == "ar";
      this.$store.dispatch("preferences/set", { lang });
    }
  }
};
</script>
