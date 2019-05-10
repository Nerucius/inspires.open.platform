<template>
  <v-layout row wrap justify-center>
    <v-flex xs12 md10 xl8>
      <v-card flat>
        <v-card-text>
          <h1 class="mb-2">
            {{ $t('pages.about.mainTitle') }}
          </h1>

          <h2 class="mb-2">
            {{ $t('pages.about.titleMission') }}
          </h2>

          <v-layout>
            <v-flex md9>
              <p class="subheading">
                {{ $t('pages.about.missionParagraph1') }}
              </p>
              <p>
                {{ $t('pages.about.missionParagraph2') }}
              </p>

              <ul class="mb-2">
                <li>
                  {{ $t('pages.about.missionObjective1') }}
                </li>
                <li>
                  {{ $t('pages.about.missionObjective2') }}
                </li>
                <li>
                  {{ $t('pages.about.missionObjective3') }}
                </li>
              </ul>
            </v-flex>
            <v-flex md3>
              <v-img src="/img/branding/inspires.png" />
            </v-flex>
          </v-layout>

          <p>
            {{ $t('pages.about.missionParagraph3') }}
          </p>

          <h2 class="mb-2">
            {{ $t('pages.about.titleTeam') }}
          </h2>

          <vue-markdown>{{ $t('pages.about.teamContent') }}</vue-markdown>

        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import VueMarkdown from 'vue-markdown';

export default {
  name: "About",

  components:{
    VueMarkdown
  },

  metaInfo: {
    title: "About Us"
  },
  components: {},
  data() {
    return {};
  }
};
</script>
