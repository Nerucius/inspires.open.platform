<style scoped>
  input[type="file"] {
    display: none;
  }
  .custom-file-upload {
    height: auto;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
  }
  .custom-file-upload > * {
    flex: 0;
  }
</style>


<template>
  <div class="mb-3">
    <v-layout col wrap>
      <v-flex xs12 sm6>
        <h4>{{ $t('components.ImageUpload.title') }}</h4>
        <label class="mb-3 v-input v-btn v-btn--block custom-file-upload" for="file">
          <div>
            <v-icon left>
              cloud_upload
            </v-icon>
            <span v-if="!file">
              {{ $t('components.ImageUpload.selectFile') }}
            </span>
            <span v-else>
              {{ $t('components.ImageUpload.fileReady', {name: file.name}) }}
            </span>
          </div>
        </label>
        <input id="file" ref="file" type="file" @change="handleFileUpload()">
        <v-btn block color="primary" :disabled="file == null" @click="submitFile()">
          {{ $t('components.ImageUpload.upload') }}
        </v-btn>
      </v-flex>
      <v-flex xs12 sm6>
        <h4>{{ $t('components.ImageUpload.currentImage') }}</h4>
        <v-img aspect-ratio="2" :src="imageUrl" />
        <v-text-field
          v-model="imageUrl"
          readonly
        />
      </v-flex>
    </v-layout>
  </div>
</template>


<script>

import { API_SERVER } from "@/plugins/resource";

export default {
  props: ['value', 'title'],

  data() {
    return {
      file: null,
      imageUrl: ""
    }
  },

  mounted() {
    this.imageUrl = this.value;
  },

  methods: {
    handleFileUpload(){
      this.file = this.$refs.file.files[0];

      if(this.file.type.indexOf('image') < 0){
        this.file = null;
        this.$store.dispatch("toast/info", this.$t('forms.toasts.invalidImageType'))
      }
    },

    async submitFile(){
      // Create form data object and add file
      let formData = new FormData();
      formData.append('file', this.file);
      var imageExtension = this.file.type.split('/')[1];
      let rand = Math.random().toString(36).substring(6);
      var fileName = `${this.title}-${rand}.${imageExtension}`;

      try {
        var response = await this.$http.post(`${API_SERVER}/upload/file/${fileName}`,
          formData, { headers: { 'Content-Type': 'multipart/form-data' } }
        )

        this.imageUrl = response.data.url
        this.$emit('input', this.imageUrl)
        this.$emit('change', this.imageUrl)
        // this.$store.dispatch("toast/success", this.$t('forms.toasts.uploadSuccessful'))
        this.file = null;

      } catch (error) {
        this.$store.dispatch("toast/error", {
          message: this.$t('forms.toasts.uploadError'), error
        });
      }

    }
  },
}
</script>