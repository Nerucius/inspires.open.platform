<template>
  <v-layout>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h1 class="mb-2">
            {{ $t('pages.legal.legalNoticeTitle') }}
          </h1>
          <vue-markdown>{{ $t('pages.legal.legalNotice') }}</vue-markdown>

          <h1 class="mb-2">
            {{ $t('pages.legal.conditionsOfUseTitle') }}
          </h1>
          <vue-markdown>{{ $t('pages.legal.conditionsOfUse') }}</vue-markdown>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  metaInfo() {
    return {
      title: this.$t('pages.legal.legalNoticeTitle')
    };
  }
};
</script>

