<style scoped>
.btn-rows .v-btn{
  margin: 18px 0px;
}
</style>

<template>
  <v-layout row wrap align-content-start>

    <v-flex xs12 sm12 md6>
      <v-card>
        <v-parallax src="/img/bg-homepage-2.jpg" height="400">
          <v-layout ma-0 pa-0 fill-height column justify-space-between>

            <v-flex shrink>
              <!-- <v-parallax height="165" src="/img/bg-homepage.jpg"> -->
              <h1 class="text-truncate mb-3">
                {{ $t('pages.home.mainTitle') }}
              </h1>
              <p class="subheading pa-1 ma-0" style="background-color:rgba(0,0,0,0.4)">
                {{ $t('pages.home.welcomeMessage') }}
              </p>
            </v-flex>

            <v-flex shrink class="btn-rows" pb-2>
              <v-layout row class="text-xs-center" style="background-color:rgba(0,0,0,0.4)">
                <v-flex xs12>
                  <h3 class="text-no-wrap">{{ $t('pages.home.useThePlatform') }}</h3>
                  <v-btn flat dark outline block :to="{name:'register'}">
                    {{ $t('pages.login.registerCTA') }}
                  </v-btn>
                  <v-btn flat dark outline block :to="{name:'project-create'}">
                    {{ $t('pages.projectCreate.title') }}
                  </v-btn>
                </v-flex>

                <v-flex xs12 class="hidden-xs-only hidden-md-only">
                  <h3>{{ $t('pages.home.learnMore') }}</h3>
                  <v-btn flat dark outline block :to="{name:'help', query:{master: 10}}">
                    {{ $t('noums.evaluation') }}
                  </v-btn>
                  <v-btn flat dark outline block :to="{name:'about'}">
                    {{ $t('navigation.links.about') }}
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-flex>

          </v-layout>
        </v-parallax>
      </v-card>
    </v-flex>

    <v-flex xs12 sm12 md6>
      <v-card :key="homeVideoURL">
        <iframe width="100%" height="400px"
                style="margin-bottom:-6px"
                :src="homeVideoURL"
                title="Inspires Open Platform" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen
        />
      </v-card>
    </v-flex>

    <!-- World map -->
    <v-flex xs12 md8>
      <h1 class="mb-2">
        {{ $t('pages.home.worldmapTitle') }}
      </h1>
      <v-card>
        <div id="world-map" style="height:400px" />
      </v-card>
    </v-flex>

    <!-- Most Active structures -->
    <v-flex xs12 md4>
      <h1 class="mb-2">
        {{ $t('pages.home.mostActiveStructures') }}
      </h1>
      <v-card>
        <v-sheet style="max-height: 400px; overflow-y:auto">
          <ModelList :objects="structures" />
        </v-sheet>
      </v-card>
    </v-flex>

    <!-- Country filter cards -->
    <v-flex v-if="countryFilterProjects" xs12>
      <h1>
        {{ countryFilter }}
        <v-btn color="grey lighten-2" class="elevation-0" @click="countryFilterProjects=null">
          <v-icon left>clear</v-icon> {{ $t('actions.clearFilter') }}
        </v-btn>
      </h1>
      <div class="hidden-sm-and-down">
        <ProjectGrid :hide-title="true" :projects="countryFilterProjects" />
      </div>
      <div class="hidden-md-and-up">
        <v-card>
          <ModelList :objects="countryFilterProjects" />
        </v-card>
      </div>
    </v-flex>

    <v-flex v-else xs12>
      <h1 class="mb-2">{{ $t('pages.home.latestProjectsTitle') }}</h1>
      <div class="hidden-sm-and-down">
        <ProjectGrid :hide-title="true" :projects="projects" />
      </div>
      <div class="hidden-md-and-up">
        <v-card>
          <ModelList show-last-modified="true" :objects="projects" />
        </v-card>
      </div>
    </v-flex>

    <v-flex class="text-xs-center">
      <v-btn large color="primary" :to="{name:'project-list'}">
        {{ $t('pages.home.projectsSeeMore') }}
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import ProjectGrid from "@/components/project/ProjectGrid";
import ModelList from "@/components/generic/ModelList";
// import { GeoJSONCountries } from "@/plugins/i18n";
import { GeoJSONCountriesDetail, Countries } from "@/plugins/i18n";
import { flatten } from "lodash";

export default {
  components: {
    ProjectGrid,
    ModelList,
  },

  data() {
    return {
      worldMap: null,
      countryFilter: null,
      countryFilterProjects: null,
    };
  },

  computed: {
    projects() {
      let projectList = this.$store.getters["project/all"].slice()
      projectList.sort((a,b) => b.modified_at.localeCompare(a.modified_at))
      return projectList.slice(0, 12);
    },
    structures(){
      let structureList = this.$store.getters["structure/all"].slice()
      structureList.sort((a,b) => b.collaborations.length - a.collaborations.length)
      // Anmotate with Number of projects in the "summary" field
      structureList = structureList.map(s => ({
        ...s,
        summary: this.$t("misc.registeredProjects", {n:s.collaborations.length})
      }))
      return structureList.slice(0,8)
    },
    homeVideoURL(){
      if(this.$i18n.locale == 'es' || this.$i18n.locale == 'ca')
        return 'https://www.youtube.com/embed/VwWsHhAJIDQ';
      return 'https://www.youtube.com/embed/VrfG2oOrSVE';
    }
  },

  async created(){
    // Load all projects (we only show the first page)
    this.$store.dispatch("structure/load")
    await this.$store.dispatch("project/load")

    setTimeout(() => {
      // Create Leaflet map
      this.createMap()
    }, 50);
  },

  methods: {
    createMap(){
      let allProjects = this.$store.getters['project/all']

      // To support multiple countries per project, split the country code, then flatten the array
      let projectCCs = allProjects.map(p => p.country_code.split(','))
      projectCCs = flatten(projectCCs)

      GeoJSONCountriesDetail.features = GeoJSONCountriesDetail.features.filter(feature =>
        projectCCs.indexOf(feature.properties.ISO_A3) >= 0
      )

      // Count number of projects per country
      GeoJSONCountriesDetail.features.map(feature => {
        feature.properties.project_count = projectCCs.filter(cc => cc == feature.properties.ISO_A3).length
      })
      let maxProjectPerCountry = Math.max(...GeoJSONCountriesDetail.features.map(f => f.properties.project_count))


      function getColor (value) {
        return `rgba(0,121,107,${(value * .9 / maxProjectPerCountry) +0.2})`;
      }


      function style(feature) {
          return {
              fillColor: getColor(feature.properties.project_count),
              weight: 2,
              opacity: 1,
              // color: 'rgb(0,121,107)',
              color: 'white',
              // dashArray: '3',
              fillOpacity: 1
          };
      }

      let _this = this

      function onEachFeature(feature, layer){
        layer.on({
            click: _this.clickOnCountry
        });
      }

      let mapUrlWatercolor = 'https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg'
      let mapUrlOficial = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

      this.worldMap = L.map('world-map',{
        maxBounds: [ [80,  -180], [-70, 180] ],
        zoomControl: false,
        zoom: 2,
        minZoom:2,
        maxZoom:5,
        center: {lat: 30, lon:0}
      })

      L.tileLayer(mapUrlWatercolor, {
          attribution: `
            <small>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
            | &copy; <a href="http://maps.stamen.com">Stamen Design</a></small>`
      }).addTo(this.worldMap);
      L.geoJson(GeoJSONCountriesDetail, {style, onEachFeature}).addTo(this.worldMap);

    },


    async clickOnCountry({target}){
      // zoom on region
      // this.worldMap.fitBounds(target.getBounds());
      let feature = target.feature
      let country_code = feature.properties.ISO_A3

      let countryItem = Countries.filter(c => c.alpha3Code == country_code)[0]
      let countryLocaleName = countryItem.translations[this.$i18n.locale]

      // Set country name
      this.countryFilter = feature.properties.NAME
      if(countryLocaleName){
        this.countryFilter = countryLocaleName
      }

      this.countryFilterProjects = await this.$store.dispatch("project/search", {country_code})
      this.countryFilterProjects.sort( (a,b) => { return a.name.localeCompare(b.name) })
    }
  }
};
</script>

