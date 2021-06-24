<style scoped>
  .content-card{
    height: 200px;
    color: white;
  }

  .content-card hr {
    margin-top: 8px;
    border-width: 2px;
    border-color: white;
  }

  h3.content-title{
    text-transform: uppercase;
    font-size: 120%;
    text-align: center;
  }

  .module--summary {
    max-height: 42px;
    overflow: hidden;
    line-height: 170%
  }
</style>

<template>
  <div v-if="modules">

    <!--
    <v-toolbar dense flat dark color="orange darken-3">
      <v-toolbar-title>
        {{ $t('pages.help.courses.modules') }}
      </v-toolbar-title>
    </v-toolbar>
    -->

    <v-layout wrap my-0>
      <v-flex v-for="content in modules" :key="content.id" pa-3 xs12 sm6 lg4>

        <v-card class="content-card" :to="content.link" flat :style="{'background-color':content.theme_color}">

          <v-layout align-space-around justify-space-between column fill-height>
            <v-flex shrink px-5 pt-3 pb-0>
              <!-- Title and text card, please note how we use a ref to get the title height -->
              <h3 :ref="content.slug+'-title'" class="content-title">{{ content.title }}</h3>
              <hr class="mb-2">
              <div class="module--summary px-1 text-xs-center">
                {{ content.summary | ellipsis(90) }}
              </div>
            </v-flex>
            <v-flex shrink px-5 pt-0><v-btn block class="elevation-0" color="white">Learn more</v-btn></v-flex>
          </v-layout>

        </v-card>

      </v-flex>


    </v-layout>

  </div>
</template>

<script>
export default {
  props: ["modules"],

  data(){
    return {}
  },

  mounted() {
    // Force remount to refresh refs
    this.$nextTick(() => { this.$mount() })
  },

  methods: {
    refHeight(ref){
      let refArray = this.$refs[ref]
      if (!refArray || refArray.length == 0) return 25;
      console.log("found ref " + ref)
      return refArray[0].offsetHeight
    }
  },
}
</script>

<style>

</style>
