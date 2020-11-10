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

        <flag :iso="getFlagIso(lang)" :squared="false" style="width:40px" />
      </v-list-tile>
    </v-list>
  </v-menu>
</template>


<script>
import { ListOfLocales, getFlagIso } from "@/plugins/i18n";


export default {
  name: "LanguageSelector",

  data() {
    return {
      ListOfLocales,
      getFlagIso
    };
  },

  computed: {
    currentLanguage() {
      return this.$store.getters["preferences/lang"];
    }
  },

  created() {
    // Reset the language
    this.$store.dispatch("preferences/set", { lang:this.currentLanguage });
  },

  methods: {
    selectLanguage(lang) {
      this.$store.dispatch("preferences/set", { lang });
    }
  }
};
</script>
