<template>
  <v-layout row wrap align-content-start>
    <v-flex xs12>
      <v-card flat>
        <v-parallax
          height="165"
          src="/img/bg-homepage.jpg"
        >
          <div>
            <h1 class="text-truncate mt-2 mb-2">
              {{ $t('pages.home.mainTitle') }}
            </h1>
            <v-sheet :height="2*21" class="hidden-xs-only transparent white--text overflow-hidden mb-2">
              {{ $t('pages.home.welcomeMessage') }}
            </v-sheet>
            <p class="text-xs-right ma-0">
              <v-btn flat outline dark :to="{name:'about'}">
                {{ $t('pages.home.aboutLink') }}
              </v-btn>
            </p>
          </div>
        </v-parallax>
      </v-card>
    </v-flex>

    <v-flex md8 sm12>
      <h1 class="mb-2">{{ $t('pages.home.worldmapTitle') }}</h1>
      <v-card>
          <div id="world-map" style="height:400px" />
      </v-card>
    </v-flex>

    <v-flex md4 class="hidden-sm-and-down">
      <h1 class="mb-2">{{ $t('pages.home.latestTitle') }}</h1>
      <v-card>
        <v-sheet height="400" style="overflow-y:auto">
        <ProjectList :projects="projects" />
        </v-sheet>
      </v-card>
    </v-flex>

    <v-flex xs12 v-if="countryFilterProjects">
      <h2>
        Projects in {{countryFilter}}
        <v-btn small color="grey lighten-2" class="elevation-0" @click="countryFilterProjects=null">
          <v-icon left>clear</v-icon>Clear filter
        </v-btn>
      </h2>
      <ProjectGrid :hide-title="true"  :projects="countryFilterProjects" />
    </v-flex>

    <v-flex xs12 v-else>
      <h2>All Projects</h2>
      <ProjectGrid :hide-title="true"  :projects="projects" />
    </v-flex>

    <v-flex class="text-xs-center">
      <v-btn large color="primary" to="/projects">
        {{ $t('pages.home.projectsSeeMore') }}
      </v-btn>
    </v-flex>

    <!--
    <v-flex xs12>
      <ProjectGrid :hide-title="true" :projects="projects" />
      <p class="text-xs-center mt-3">
        <v-btn large dark color="primary" :to="{name:'project-list'}">
          {{ $t('pages.home.projectsSeeMore') }}
        </v-btn>
      </p>
    </v-flex> -->


  </v-layout>
</template>

<script>
import ProjectGrid from "@/components/project/ProjectGrid";
import ProjectList from "@/components/project/ProjectList";
// import { GeoJSONCountries } from "@/plugins/i18n";
import { GeoJSONCountriesDetail } from "@/plugins/i18n";

export default {
  components: {
    ProjectGrid,
    ProjectList,
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
      return this.$store.getters["project/all"];
    }
  },

  async created(){
    await this.$store.dispatch("project/load", {params:{limit:999}})

    setTimeout(() => {
      // Create Leaflet map
      this.createMap()
    }, 50);


  },

  methods: {
    createMap(){

      let projectCCs = this.projects.map(p => p.country_code)

      GeoJSONCountriesDetail.features = GeoJSONCountriesDetail.features.filter(feature =>
        projectCCs.indexOf(feature.properties.ISO_A3) >= 0
      )

      // Count number of projects per country
      GeoJSONCountriesDetail.features.map(feature => {
        feature.properties.project_count = projectCCs.filter(cc => cc == feature.properties.ISO_A3).length
      })
      let maxProjectPerCountry = Math.max(...GeoJSONCountriesDetail.features.map(f => f.properties.project_count))


      function getColor (value) {
        return `rgba(0,121,107,${value * .9 / maxProjectPerCountry})`;
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

      let mapUrlWatercolor = 'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg'
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
          attribution: '<small>&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors</small>'
      }).addTo(this.worldMap);
      L.geoJson(GeoJSONCountriesDetail, {style, onEachFeature}).addTo(this.worldMap);

    },


    async clickOnCountry({target}){
      // zoom on region
      // this.worldMap.fitBounds(target.getBounds());
      let feature = target.feature
      let country_code = feature.properties.ISO_A3

      this.countryFilter = feature.properties.NAME
      this.countryFilterProjects = await this.$store.dispatch("project/search", {country_code})
    }
  }
};
</script>

