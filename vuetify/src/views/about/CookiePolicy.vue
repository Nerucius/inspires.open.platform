<template>
  <v-layout>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h1 class="mb-2">
            {{ $t('pages.legal.cookiePolicyTitle') }}
          </h1>
          <vue-markdown>{{ $t('pages.legal.cookiePolicy') }}</vue-markdown>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  metaInfo() {
    return {
      title: this.$t('pages.legal.cookiePolicyTitle')
    };
  }
};
</script>
