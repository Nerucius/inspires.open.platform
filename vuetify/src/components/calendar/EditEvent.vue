<template>

  <v-dialog
    max-width="600px"
    v-model="dialog">
    <v-btn icon slot="activator">
      <v-icon>edit</v-icon>
    </v-btn>

      <v-card class="" v-if="editedEvent">
        <v-toolbar dark color="primary" class="elevation-0">
          <v-toolbar-title>edit event</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
          </v-toolbar-items>
        </v-toolbar>

        <v-card-text>
          <v-form
            ref="form"
            v-model="valid"
            @keyup.native.enter="valid && saveEvent()"
            @submit.prevent="saveEvent()"
          >

            <v-layout>
              <v-flex xs5>
                <FieldDatePicker
                  label="Pick event Date"
                  :date="format(event.date_start, 'YYYY-MM-DD')"
                  @change="changeDateStart($event)"
                  ></FieldDatePicker>
              </v-flex>
              <v-spacer></v-spacer>
              <v-flex xs5>
                <FieldTimePicker
                  label="Pick event Time"
                  :time="format(event.date_start, 'HH:mm')"
                  @change="changeTimeStart($event)"
                  ></FieldTimePicker>
              </v-flex>
            </v-layout>

            <v-text-field
              ref="usernameInput"
              v-model="editedEvent.title"
              label="Event title"
              :rules="rules"
            ></v-text-field>

            <v-textarea
              v-model="editedEvent.content"
              label="Event content"
              :rules="rules"
            ></v-textarea>


          </v-form>
        </v-card-text>
        <v-card-actions class="pb-3 pr-3">
          <v-btn @click="dialog=false" flat >
            {{ $t("actions.cancel") }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn @click="saveEvent()" :disabled="!valid" color="primary">
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
  props: ["event"],

  components:{
    FieldDatePicker,
    FieldTimePicker,
  },

  data() {
    return {
      dialog: null,
      format: format,
      valid: null,
      editedEvent: null,
      rules: [v => !!v || this.$t("forms.rules.requiredField")]
    };
  },
  mounted() {
    this.editedEvent = {...this.event}
  },
  methods: {

    resetForm() {
      this.$refs.form.reset();
    },

    changeDateStart(newDate){
      let [y,m,d] = newDate.split('-').map(v => parseInt(v, 10))
      let date_start = this.editedEvent.date_start
      date_start = setYear(date_start, y)
      date_start = setMonth(date_start, m-1)
      date_start = setDate(date_start, d)
      this.editedEvent.date_start = format(date_start)
    },

    changeTimeStart(newTime){
      let [h, m] = newTime.split(':').map(v => parseInt(v, 10))
      let date_start = this.editedEvent.date_start
      date_start = setHours(date_start, h)
      date_start = setMinutes(date_start, m)
      this.editedEvent.date_start = format(date_start)
    },

    saveEvent() {
      if (this.$refs.form.validate()) {
        this.editedEvent.date_end = format(addHours(this.editedEvent.date_start, 1))
        this.$store.dispatch("calendarEvent/update", this.editedEvent)
        this.dialog = false
      }
    },
  },

  computed: {

  }
};
</script>
