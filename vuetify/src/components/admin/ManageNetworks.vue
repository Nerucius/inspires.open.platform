<template>
  <v-card flat>
    <v-card-text>
      <h2 class="mb-2">Structure Networks</h2>
      <p class="subheading">
        Create or Modify the National or International networks here.
      </p>

      <v-list two-line>
        <template v-for="(network, idx) in networks">
          <v-list-tile :key="network.id">
            <v-list-tile-avatar tile size="60" class="mr-2">
              <v-icon large>mdi-graphql</v-icon>
            </v-list-tile-avatar>

            <!-- Tile content -->
            <v-list-tile-content>
              <v-list-tile-title>
                <strong>{{ network.name }}</strong>
              </v-list-tile-title>
              <v-list-tile-sub-title>
                {{ network.summary }}
              </v-list-tile-sub-title>
            </v-list-tile-content>

            <v-list-tile-action>
              <v-btn
                color="orange"
                icon
                ripple
                class="ml-1"
                :href="editNetworkLink(network)"
                target="_blank"
              >
                <v-icon color="white">edit</v-icon>
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>

          <v-divider
            v-if="idx != networks.length - 1"
            :key="`div-${network.id}`"
            inset
          />
        </template>
      </v-list>

      <v-btn block color="success" outline :href="createNetworkLink" target="_blank">
        <v-icon left>add</v-icon> Create new Network
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
import { API_SERVER } from "@/plugins/resource";

export default {
  computed:{
    createNetworkLink(){
      return `${API_SERVER}/admin/backend/network/add/`;
    },
    networks(){
      return this.$store.getters['network/all']
    }
  },

  async created(){
    this.$store.dispatch('network/load')
  },

  methods: {
    editNetworkLink(network){
      return `${API_SERVER}/admin/backend/network/${network.id}/change/`;
    }
  },

}
</script>

<style>

</style>
