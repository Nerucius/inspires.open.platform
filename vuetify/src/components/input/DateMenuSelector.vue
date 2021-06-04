<template>
  <v-menu
    ref="menu"
    v-model="menu"
    :close-on-content-click="false"
    :nudge-right="40"
    :return-value.sync="date"
    lazy
    transition="scale-transition"
    offset-y
    full-width
    min-width="290px"
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        v-model="date"
        box
        :label="label"
        :rules="rules"
        prepend-icon="event"
        readonly
        v-on="on"
      />
    </template>
    <v-date-picker v-model="date" no-title scrollable :locale="currentLanguage">
      <v-spacer />
      <v-btn flat color="primary" @click="menu = false">Cancel</v-btn>
      <v-btn flat color="primary" @click="$refs.menu.save(date) & emitChange()">OK</v-btn>
    </v-date-picker>
  </v-menu>
</template>

<script>
  export default {
    props: ['value', 'label', 'rules'],

    data: () => ({
      date: null,
      menu: false,
    }),

    computed: {
      currentLanguage() {
        return this.$store.getters["preferences/lang"];
      }
    },

    mounted(){
      this.date = this.value
    },

    methods: {
      emitChange(){
        this.$emit('input', this.date)
        this.$emit('change', this.date)
      }
    },
  }
</script>
