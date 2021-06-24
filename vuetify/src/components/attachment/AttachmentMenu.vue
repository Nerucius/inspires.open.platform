<template>
  <v-expansion-panel v-model="panels[0]" class="elevation-0">
    <v-expansion-panel-content>
      <!-- Trigger Slot -->
      <template v-slot:header>
        <h1 class="title">{{ $t('pages.help.courses.recomendedMaterials') }} ({{ content.attachments.length }})</h1>
      </template>

      <v-sheet class="grey lighten-4 pa-4">
        <!-- List of attachments -->
        <AttachmentList :attachments="content.attachments" @change="onChange" />
        <!-- Upload form for editor -->
        <template v-if="currentUser.is_editor">
          <br>
          <br>
          <h3 mb-2>{{ $t('components.Attachment.upload') }}</h3>
          <AttachmentUpload model="content" :object-id="content.id" @upload="onChange" />
        </template>
      </v-sheet>

    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import AttachmentUpload from "@/components/input/AttachmentUpload";
import AttachmentList from "@/components/attachment/AttachmentList";

export default {
  components: {
    AttachmentList,
    AttachmentUpload,
  },

  props: ["content", "expanded"],

  data(){
    return{
      panels: []
    }
  },

  computed:{
    currentUser(){
      return this.$store.getters['user/current']
    },
  },

  created(){
    if(this.expanded != undefined && this.expanded != false){
      this.panels = [0]
    }
  },

  methods : {
    onChange(){
      this.$emit('change')
    }
  }
}
</script>
