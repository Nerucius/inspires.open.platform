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

          <!-- Mission -->
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

          <!-- Team behind inspires -->
          <h2 class="mb-2">
            {{ $t('pages.about.titleTeam') }}
          </h2>
          <vue-markdown>{{ $t('pages.about.teamContent') }}</vue-markdown>

          <!-- Partners -->
          <h2 class="mb-2">
            {{ $t('pages.about.titlePartners') }}
          </h2>
          <vue-markdown>{{ $t('pages.about.partnersContent') }}</vue-markdown>

          <v-layout row wrap align-content-start>
            <v-flex v-for="partner in partners" :key="partner.name" sm6 md4 mb-3>
              <v-card flat class="ma-2" style="overflow: visible">
                <!-- Regular image view -->
                <v-img
                  contain
                  :src="partner.image_url"
                  height="180"
                />

                <v-card-text class="pb-0">
                  <v-sheet :height="5*21" class="overflow-hidden mb-2">
                    <!-- Project Title -->
                    <h2 style="font-size:125%" class="mb-2 text-xs-center">
                      {{ partner.name }}
                    </h2>
                  </v-sheet>
                </v-card-text>


                <v-card-actions>
                  <v-btn flat block :href="partner.url">{{ $t('pages.projectDetail.detailsTab') }}</v-btn>
                  <v-btn v-if="partner.structure_link" flat block :to="partner.structure_link">{{ $t('noums.structure') }}</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>

          <!-- ContactUs Form -->
          <h2 class="mb-2">
            {{ $t('pages.about.contactUsTitle') }}
          </h2>

          <ContactForm feedback-type="CONTACT_US" />

        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import ContactForm from "@/components/input/ContactForm";

export default {

  metaInfo() {
    return {
      title: this.$t('pages.about.mainTitle')
    };
  },

  components: {
    ContactForm
  },

  data() {
    return {
      partners:[
      {
        name: "ISGlobal - Barcelona Institute for Global health",
        country: "Spain",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/ISGlobal_Logo.png",
        url: "https://inspiresproject.com/isgpartners/barcelona-institute-for-global-health-inspires-coordintaror/",
        structure_link: {name:"structure-detail", params:{slug:'1-isglobal-science-shop'}}
      },
      {
        name: "ESSRG - Environmental Social Sciences Research Groups Ltd",
        country: "Hungary",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/ESSRG_Logo.png",
        url: "https://inspiresproject.com/isgpartners/environmental-social-sciences-research-groups-ltd-essrg/",
        structure_link: {name:"structure-detail", params:{slug:'4-essrg'}}
      },
      {
        name: "IRSICaixa - Fundación Privada Institut de Recerca de la Sida-Caixa",
        country: "Spain",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/IRSI_Logo.png",
        url: "https://inspiresproject.com/isgpartners/fundacion-privada-institut-de-recerca-de-la-sida-caixa-irsicaixa/",
        structure_link: {name:"structure-detail", params:{slug:'22-living-lab-for-health-at-irsicaixa'}}
      },
      {
        name: "UDL - Université de Lyon",
        country: "France",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/ULyon_Logo.png",
        url: "https://inspiresproject.com/isgpartners/universite-de-lyon-udl/",
        structure_link: {name:"structure-detail", params:{slug:'15-universit-de-lyon-udl'}}
      },
      {
        name: "VU - The VU Institute for research on innovation and communication in the health and life sciences",
        country: "___",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/VU_Logo.png",
        url: "https://inspiresproject.com/isgpartners/the-vu-institute-for-research-on-innovation-and-communication-in-the-health-and-life-sciences-vu/",
        // structure_link: {name:"structure-detail", params:{slug:'__'}}
      },
      {
        name: "UNIFI - Università degli studi di Firenze",
        country: "Italy",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/UNIFI-NUOVO_Logo.png",
        url: "https://inspiresproject.com/isgpartners/universita-degli-studi-di-firenze-unifi/",
        structure_link: {name:"structure-detail", params:{slug:'2-university-of-florence'}}
      },
      {
        name: "IPT - Institut Pasteur Tunis",
        country: "Tunisia",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/IPTunis_Logo.png",
        url: "https://inspiresproject.com/isgpartners/institut-pasteur-tunis-ipt/",
        structure_link: {name:"structure-detail", params:{slug:'16-institut-pasteur-de-tunis'}}
      },
      {
        name: "CEADES - Ciencia y estudios aplicados para el desarrollo en salud y medio ambiente",
        country: "Bolivia",
        image_url: "https://inspiresproject.com/wp-content/uploads/2017/11/CEADES_logopng-e1509794576720.png",
        url: "https://inspiresproject.com/isgpartners/ciencia-y-estudios-aplicados-para-el-desarrollo-en-salud-y-medio-ambiente-ceades/",
        structure_link: {name:"structure-detail", params:{slug:'19-fundacin-ceades-en-cochabamba-bolivia'}}
      },
      {
        name: "Living Knowledge - The International Science Shop Network",
        country: "International",
        image_url: "/img/branding/lk_logo_text_512.png",
        url: "https://www.livingknowledge.org/",
        // structure_link: {name:"structure-detail", params:{slug:'19-fundacin-ceades-en-cochabamba-bolivia'}}
      },
      {
        name: "FIOCRUZ - Oswaldo Cruz Foundation",
        country: "International",
        image_url: "https://divulgaempregos.com.br/wp-content/uploads/2018/10/338664562_Fiocruz_logo_452.png",
        url: "https://portal.fiocruz.br/en",
        // structure_link: {name:"structure-detail", params:{slug:'19-fundacin-ceades-en-cochabamba-bolivia'}}
      },
      ]
    };
  }
};
</script>
