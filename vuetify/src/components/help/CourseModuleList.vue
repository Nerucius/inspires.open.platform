<style scoped>
  .content-card{
    height: 100px;
    color: white;
  }

  .content-card hr {
    margin-top: 8px;
    border-width: 2px;
    border-color: inherit;
  }

  h3.content-title{
    text-transform: uppercase;
    font-size: 120%;
    text-align: center;
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

          <v-layout align-center justify-center fill-height>
            <v-flex shrink px-5>
              <!-- Title and text card, please note how we use a ref to get the title height -->
              <h3 :ref="content.slug+'-title'" class="content-title">{{ content.title }}</h3>
              <!-- <v-sheet :height="164 - refHeight(content.slug+'-title')" class="pr-3" style="overflow-y:auto; line-height: 170%">
                {{ content.summary }}
              </v-sheet> -->
              <hr>
            </v-flex>
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
      if (refArray == null || refArray.length == 0) return 24;
      return refArray[0].offsetHeight
    }
  },
}
</script>

<style>

</style>
