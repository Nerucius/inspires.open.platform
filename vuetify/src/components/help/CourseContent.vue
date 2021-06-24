<style>
  .v-expansion-panel__header{
    font-size: 140%;
    padding: 0;
    flex-direction: row-reverse;
  }

  .v-expansion-panel__header__icon{
    width: 48px;
    text-align: center;
    font-size: 120%;
    background-color: transparent;
  }

  .v-expansion-panel__container > *{
    margin: -1.5px;
  }

  .course-markdown table tr{
    display: flex;
  }
  .course-markdown table td{
    flex: 0 0 1fr;
  }

</style>

<style>
/* Generic Style */
.course-markdown {
  line-height: 180% !important;
  font-size: 110% !important;

  --title1Color: darkblue;
  --title2Color: teal;
  --title3Color: darkblue;
  --title3NumberColor: white;
  --title3NumberBG: darkblue;

  --lightShade: rgb(235,237,244);
  --darkShade: rgb(95,172,220);
  --bqText: white;
  --bqBackground: rgb(48,65,147);
}

.course-markdown img{
  max-width: 100%;
}

/* Titles */
.course-markdown h1 {
  font-size: 160% !important;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  color: var(--title1Color);
  margin: 40px 0;
}

.course-markdown h2 {
  font-size: 140% !important;
  letter-spacing: 2px;
  color:white;
  /* color: var(--title2Color); */
  margin: -16px;
  padding: 24px;
}

.course-markdown h3 {
  text-transform: uppercase;
  padding: 12px 12px 12px 18px;
  line-height: 100%;
  color: var(--title3Color);
}


.course-markdown p{
  margin: 0;
  padding: 15px 0;
  text-align: justify;
}

.course-markdown blockquote{
  border-left: 3px solid darkslategray;
  padding-left: 15px;
  margin: 15px 0;
}

.course-markdown table{
  width: 100%;
  text-align: justify;
  border-spacing: 0;
}

/* Flex tables for equal columns */
.course-markdown table tr{
  display: flex;
}

.course-markdown table td, .course-markdown table th{
  flex: 1 0 0;
}

.course-markdown table th:empty{
  height: 0px;
  margin: 0px;
  padding: 0px;
}

.course-markdown table th{
  background-color: rgb(37, 153, 212);
  color: snow;
  font-size: 110%;
}

.course-markdown table th, .course-markdown table td{
  padding: 12px;
}
</style>

<template>
  <div :dir="localeDir">

    <!-- Course Content -->
    <div v-for="(section, i) in sections" :key="'section-'+i" flat class="my-5">
      <v-expansion-panel v-model="panels[i]" class="elevation-0">

        <v-expansion-panel-content>
          <template v-slot:header>
            <v-sheet flat dark :color="content.theme_color" class="pa-2 ma-0">
              {{ section.title }}
            </v-sheet>
          </template>
          <template v-slot:actions>
            <v-icon large :color="content.theme_color">$vuetify.icons.expand</v-icon>
          </template>
          <v-card-text>
            <vue-markdown :class="['course-markdown', content.extra_style]">{{ section.body }}</vue-markdown>
          </v-card-text>
        </v-expansion-panel-content>

      </v-expansion-panel>

    </div>

  </div>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n";

export default {

  components:{
  },

  props : ["content", "parent", "contentsSameMaster"],

  data(){
    return {
      moment,
      panels: [0],
      viewAsPDF: false,
      getFlagIso,
    }
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
    localeDir(){
      if (this.content.locale == 'ar') return 'rtl';
      return 'ltr';
    },
    sections(){
      return this.splitIntoSections()
    }
  },

  created() {
  },

  methods: {

    splitIntoSections(){
      var sections = [];

      if(!this.content || !this.content.body)
        return sections

      // Split the content along '---'
      var sectionSplits = this.content.body.split('---').map(s => s.trim())

      // Convert each section to have its own title
      sectionSplits.forEach(sec => {
        var title, body
        var firstLine = sec.split('\n')[0]
        if(firstLine.startsWith('#')){
          title = firstLine.replaceAll('#','');
          body = sec.replace(firstLine,'')
        }else{
          title = 'Section'
          body = sec
        }
        sections = [...sections, {title, body}]
      });
      return sections;
    }

  },

}
</script>
