<template>
  <v-dialog
    v-model="dialog"
    max-width="600px"
  >
    <v-btn slot="activator" absolute right bottom fab dark color="success">
      <v-icon>add</v-icon>
    </v-btn>

    <v-card class="">
      <v-toolbar dense dark color="primary" class="elevation-0">
        <v-toolbar-title>
          <v-icon left>
            calendar_today
          </v-icon>
          Add event
        </v-toolbar-title>
        <v-spacer />
        <v-toolbar-items />
      </v-toolbar>

      <v-card-text>
        <v-form
          ref="form"
          v-model="valid"
          @keyup.native.enter="valid && saveEvent()"
          @submit.prevent="saveEvent()"
        >
          <v-text-field
            v-model="addedEvent.title"
            prepend-icon="edit"
            label="Event title"
            :rules="rules"
          />
          <v-textarea
            v-model="addedEvent.content"
            prepend-icon="edit"
            label="Event content"
            :rules="rules"
          />

          <v-layout>
            <v-flex xs5>
              <FieldDatePicker
                label="Pick event Date"
                :date="format(addedEvent.date_start, 'YYYY-MM-DD')"
                @change="changeDateStart($event)"
              />
            </v-flex>
            <v-spacer />
            <v-flex xs5>
              <FieldTimePicker
                label="Pick event Time"
                :time="format(addedEvent.date_start, 'HH:mm')"
                @change="changeTimeStart($event)"
              />
            </v-flex>
          </v-layout>
        </v-form>
      </v-card-text>
      <v-card-actions class="pb-3 pr-3">
        <v-btn flat @click="dialog=false">
          {{ $t("actions.cancel") }}
        </v-btn>
        <v-spacer />
        <v-btn :disabled="!valid" color="primary" @click="saveEvent()">
          {{ $t("actions.save") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import FieldDatePicker from "@/components/calendar/FieldDatePicker";
import FieldTimePicker from "@/components/calendar/FieldTimePicker";
import { format, addHours, setHours, setMinutes, setYear, setMonth, setDate} from 'date-fns';

export default {

  components:{
    FieldDatePicker,
    FieldTimePicker,
  },
  props: ["eventType"],

  data() {
    return {
      format: format,
      dialog: null,
      valid: null,
      addedEvent: {
        title: "",
        content: "",
        date_start: format(new Date()),
        date_end: format(addHours(new Date(), 1)),
        color: "blue",
        is_full_day: false,
        icon: "event",
      },
      rules: [v => !!v || this.$t("forms.rules.requiredField")]
    };
  },

  computed: {

  },


  mounted(){

    if (this.eventType == "user"){
      // User calendar event type
      this.addedEvent = {
        ...this.addedEvent,
        content_type: 6,
        content_id: this.$store.getters["user/current"].id
      }
    }
  },


  methods: {

    resetForm() {
      this.$refs.form.reset();
    },

    saveEvent() {
      if (this.$refs.form.validate()) {
        this.addedEvent.date_end = format(addHours(this.addedEvent.date_start, 1))
        this.$store.dispatch("calendarEvent/add", this.addedEvent)
        this.dialog = false
      }
    },

    changeDateStart(newDate){
      let [y,m,d] = newDate.split('-').map(v => parseInt(v, 10))
      let date_start = this.addedEvent.date_start
      date_start = setYear(date_start, y)
      date_start = setMonth(date_start, m-1)
      date_start = setDate(date_start, d)
      this.addedEvent.date_start = format(date_start)
    },

    changeTimeStart(newTime){
      let [h, m] = newTime.split(':').map(v => parseInt(v, 10))
      let date_start = this.addedEvent.date_start
      date_start = setHours(date_start, h)
      date_start = setMinutes(date_start, m)
      this.addedEvent.date_start = format(date_start)
    },
  }
};
</script>
