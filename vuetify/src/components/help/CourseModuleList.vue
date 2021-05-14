<template>
  <v-card v-if="modules" flat>
    <v-toolbar dense flat dark color="orange darken-3">
      <v-toolbar-title>
        {{ $t('pages.help.courses.modules') }}
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-layout wrap>
        <v-flex v-for="content in modules" :key="content.id" xs12 sm6 lg4>
          <v-card>
            <v-card-text>
              <!-- Title and text card, please note how we use a ref to get the title height -->
              <h3 :ref="content.slug+'-title'" class="mb-3">{{ content.title }}</h3>
              <v-sheet :height="164 - refHeight(content.slug+'-title')" class="pr-3" style="overflow-y:auto; line-height: 170%">
                {{ content.summary }}
              </v-sheet>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn flat color="primary" :to="content.link">Access Module</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ["modules"],

  mounted() {
    // Force remount to refresh refs
    this.$nextTick(() => { this.$mount() })
  },

  methods: {
    refHeight(ref){
      let refArray = this.$refs[ref]
      if (refArray == null || refArray.length == 0) return 24;
      return refArray[0].offsetHeight
    }
  },
}
</script>

<style>

</style>
