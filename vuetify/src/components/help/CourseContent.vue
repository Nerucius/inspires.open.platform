<style>
/* Generic Style */
.markdown {
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

.markdown img{
  max-width: 100%;
}

/* Titles */
.markdown h1 {
  font-size: 160% !important;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
  color: var(--title1Color);
  margin: 40px 0;
}

.markdown h2 {
  font-size: 140% !important;
  letter-spacing: 2px;
  text-align: center;
  color: var(--title2Color);
  margin: 30px 0;
}

.markdown h3 {
  text-transform: uppercase;
  padding: 12px 12px 12px 18px;
  line-height: 100%;
  color: var(--title3Color);
  background-color: var(--lightShade);
}

.markdown h3::first-letter {
  display: inline-block;
  line-height: 100%;
  vertical-align: -10%;
  font-size: 160%;
  border-radius: 100%;
  font-weight: 500;
  color: var(--title3NumberColor);
  background-color: var(--title3NumberBG);
  padding: 0 8px;
  margin-right: 8px;
}

.markdown p{
  margin: 0;
  padding: 15px 0;
  text-align: justify;
}

.markdown blockquote{
  border-left: 3px solid darkslategray;
  padding-left: 15px;
  margin: 15px 0;
}

.markdown table{
  width: 100%;
  text-align: justify;
  border-spacing: 0;
}

/* Flex tables for equal columns */
.markdown table tr{
  display: flex;
}

.markdown table td, .markdown table th{
  flex: 1 0 0;
}

.markdown table th:empty{
  height: 0px;
  margin: 0px;
  padding: 0px;
}

.markdown table th{
  background-color: rgb(37, 153, 212);
  color: snow;
  font-size: 110%;
}

.markdown table th, .markdown table td{
  padding: 12px;
}
</style>

<template>
  <v-card flat>
    <!-- Toolbar -->
    <v-toolbar dense flat dark color="grey darken-3">
      <v-toolbar-title>
        <span v-if="parent" class="grey--text hidden-sm-and-down">
          {{ parent.title }} / 
        </span>
        {{ content.title }}
      </v-toolbar-title>
      <v-spacer />
      <!-- Back button -->
      <v-btn v-if="parent" flat exact :to="parent.link">
        <v-icon left>
          mdi-arrow-left
        </v-icon>{{ $t("actions.back") }}
      </v-btn>
      <v-btn v-else flat exact :to="{name:'help'}">
        <v-icon left>
          mdi-arrow-left
        </v-icon>{{ $t("actions.back") }}
      </v-btn>

      <!-- This article in other languages -->
      <v-menu v-if="contentsSameMaster.length > 0" offset-y>
        <v-btn slot="activator" flat>
          {{ content.locale }}
          <v-icon right>
            expand_more
          </v-icon>
        </v-btn>
        <v-list>
          <v-list-tile v-for="a in contentsSameMaster" :key="a.slug" :to="a.link">
            <v-list-tile-title>
              <small>{{ a.locale | uppercase }}</small>
            </v-list-tile-title>
            <flag
              :iso="getFlagIso(a.locale)"
              :squared="false"
              style="width: 40px"
            />
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>
    
    <!-- Course Content -->
    <v-card-text :dir="localeDir" :class="['markdown', content.extra_style]">
      <vue-markdown>{{ content.body }}</vue-markdown>
      <v-layout mt-3 justify-end>
        <v-flex shrink class="grey--text">
          <span :title="moment(content.modified_at).format('L LT')">
            {{
              $t("misc.lastUpdated", {
                time: moment(content.modified_at).fromNow(),
              })
            }}
          </span>
        </v-flex>
      </v-layout>
    </v-card-text>

    <!-- Attachments -->
    <v-card-text>
      <v-sheet class="grey lighten-4 pa-3">
        <h2 class="mb-2">{{ $t('noums.files') }}</h2>
        <!-- List of attachments -->
        <AttachmentList :attachments="content.attachments" @change="reloadContent" />
        <!-- Upload form for editor -->
        <template v-if="currentUser.is_editor">
          <br>
          <br>
          <h3 mb-2>{{ $t('components.Attachment.upload') }}</h3>
          <AttachmentUpload model="content" :object-id="content.id" @upload="reloadContent" />
        </template>
      </v-sheet>
    </v-card-text>

  </v-card>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n";
import AttachmentUpload from "@/components/input/AttachmentUpload";
import AttachmentList from "@/components/attachment/AttachmentList";

export default {

  components:{
    AttachmentUpload,
    AttachmentList
  },
  props : ["content", "parent", "contentsSameMaster"],

  data(){
    return {
      moment,
      getFlagIso,
      viewAsPDF: false
    }
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
    localeDir(){
      if (this.content.locale == 'ar') return 'rtl';
      return 'ltr';
    }
  },

  created() {
  },

  methods: {

    async reloadContent(){
      console.log("Reloading article")
      this.$store.dispatch('content/load', [this.content.slug])
    }

  },

}
</script>
