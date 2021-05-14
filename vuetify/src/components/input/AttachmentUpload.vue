<style scoped>
input[type="file"] {
  display: none;
}
.custom-file-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
.custom-file-upload > * {
  flex: 0;
}
.custom-file-upload span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>


<template>
  <v-form ref="form" v-model="valid" @submit.prevent="uploadAttachment">
    <v-layout wrap>
      <v-flex xs12>
        <v-text-field
          v-model="attachment.name" single-line
          hide-details
          :rules="[rules.required]"
          :label="$t('forms.fields.attachmentName')"
        />
      </v-flex>
      <v-flex xs12 sm6>
        <label
          class="v-btn v-btn--block custom-file-upload"
          for="file"
        >
          <div class="v-btn__content">
            <v-icon left>cloud_upload</v-icon>
            <span v-if="!file">
              {{
                $t("components.ImageUpload.selectFile")
              }}
            </span>
            <span v-else>{{ file.name }}</span>
          </div>
        </label>
        <input id="file" ref="file" type="file" @change="onFileChange">
      </v-flex>
      <v-flex xs12 sm6>
        <v-btn type="submit" :disabled="!valid || !file" block color="success">Upload</v-btn>
      </v-flex>
    </v-layout>
  </v-form>
</template>


<script>
import { API_SERVER } from "@/plugins/resource";

const VALID_MIME_TYPES = ["image/png", "image/jpeg", "application/pdf"];


function normalizeName(str){
  str = str.toLowerCase();
  str = str.replace(' ', '-')
  str = str.replace(/[^a-zA-Z0-9\_\-]/gi, '');

  return str.slice(0,64)
}

export default {
  props: ["model", "objectId"],

  data() {
    return {
      file: null,
      valid: null,
      contentType: null,
      attachment: {},
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
      },
    };
  },

  async mounted() {
    this.imageUrl = this.value;

    // Load contentTypes and get the one for 'content'
    await this.$store.dispatch('attachment/loadContentTypes');
    this.contentType = this.$store.getters['attachment/contentType'](this.model).id;
  },

  methods: {
    onFileChange() {
      this.file = this.$refs.file.files[0];

      console.log(this.file)

      if (VALID_MIME_TYPES.indexOf(this.file.type) < 0) {
        this.file = null;
        this.$store.dispatch(
          "toast/info",
          this.$t("forms.toasts.invalidFileType")
        );
      }
    },

    async uploadAttachment() {
      // Create form data object and add file
      let formData = new FormData();
      formData.append("file", this.file);

      let rand = Math.random().toString(36).substring(6);
      let normName = normalizeName(this.attachment.name)
      let extension = this.file.name.split('.').pop()
      let fileSize = this.file.size

      if(fileSize > 10 * 1024*1024){
        this.$store.dispatch("toast/error", {message: this.$t("forms.toasts.uploadErrorTooBig", {size:10})});
        this.file = null
        return;
      }

      var fileName = `${rand}-${normName}.${extension}`;
      console.log(fileName);

      try {
        // Attempt to upload File
        let response = await this.$http.post(
          `${API_SERVER}/upload/file/${fileName}`,
          formData, { headers: { "Content-Type": "multipart/form-data" } }
        );

        let attachmentData = {
          ...this.attachment,
          mime_type: this.file.type,
          size: fileSize,
          url: response.data.url,
          content_type: this.contentType,
          object_id: this.objectId,
        };

        await this.$store.dispatch("attachment/create", attachmentData);

        this.$store.dispatch(
          "toast/success",
          this.$t("forms.toasts.uploadSuccessful")
        );

        // Upload complete
        this.file = null;
        this.attachment = {}
        this.$refs.form.reset()

        this.$emit('upload');

      } catch (error) {
        this.$store.dispatch("toast/error", {message: this.$t("forms.toasts.uploadError"), error,});
      }
    },
  },
};
</script>
