<template>
  <v-menu
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
    <v-text-field
      slot="activator"
      v-model="innerDate"
      :label="label"
      prepend-icon="event"
      readonly
    />
    <v-date-picker
      v-model="innerDate"
      first-day-of-week="1"
      :locale="$i18n.locale"
      no-title
      scrollable
      @input="innerDate = $event; $emit('change', $event); menu=false"
    >
      <!-- <v-spacer></v-spacer>
      <v-btn flat color="primary" @click="menu = false;">OK</v-btn> -->
    </v-date-picker>
  </v-menu>
</template>

<script>
import { format } from 'date-fns';

export default {
  props: ['date', 'label'],

  data(){
    return{
      menu: false,
      innerDate: null,
    }
  },

  mounted(){
    this.innerDate = this.date
  },

}
</script>
