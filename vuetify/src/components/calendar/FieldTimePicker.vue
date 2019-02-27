<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    :nudge-right="40"
    lazy
    offset-y
    full-width
    transition="scale-transition"
    max-width="290px"
    min-width="290px"
  >
    <v-text-field
      slot="activator"
      v-model="innerTime"
      :label="label"
      prepend-icon="access_time"
      readonly
    />
    <v-time-picker
      v-if="menu"
      v-model="innerTime"
      full-width
      @input="innerTime = $event; $emit('change', $event)"
      @click:minute="menu=false"
    />
  </v-menu>
</template>


<script>
export default {
  props: ['time', 'label'],

  data(){
    return{
      menu: false,
      innerTime: null
    }
  },

  mounted(){
    this.innerTime = this.time
  }

}
</script>