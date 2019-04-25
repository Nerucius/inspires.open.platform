<template>
  <v-layout>

    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h1 class="mb-2">
            {{ $t('pages.termsOfService.mainTitle') }}
          </h1>

          <h2 class="mb-2">{{ $t('pages.termsOfService.subTitle') }}</h2>

            <p>{{ $t('pages.termsOfService.paragraph1') }}</p>
            <vue-markdown>{{ $t('pages.termsOfService.paragraph2') }}</vue-markdown>
            <p>{{ $t('pages.termsOfService.paragraph3') }}</p>
            <p>{{ $t('pages.termsOfService.paragraph4') }}</p>
            <p>{{ $t('pages.termsOfService.paragraph5') }}</p>
            <vue-markdown>{{ $t('pages.termsOfService.paragraph6') }}</vue-markdown>
            <p>{{ $t('pages.termsOfService.paragraph7') }}</p>


        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import VueMarkdown from 'vue-markdown'

export default {
  metaInfo: {
    title: "Terms of Service"
  },
  components: {VueMarkdown},
  data() {
    return {};
  }
};
</script>
