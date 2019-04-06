<template>
  <v-layout>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <h1 class="mb-2">About InSPIRES</h1>

          <h2 class="mb-2">Our Mission</h2>

          <v-layout>
            <v-flex md9>
              <p class="subheading">
                InSPIRES has embarked in the adventure of developing an online collaborative
                and crowdsourced database featuring Science Shops, similar structures and their
                related projects, as well as offering an integrated impact evaluation tool
                capable of producing real-time project evaluation report.
              </p>
              <p>The aims of the InSPIRES online database and impact evaluation are to:</p>

              <ul class="mb-2">
                <li>
                  Identify and visualize the size of the Science Shops, and other similar
                  structures, movement and similar structures worldwide
                </li>
                <li>
                  Register collaborative research and innovation projects, facilitated by
                  these intermediation structures , to show their objectives, knowledge and
                  geographical areas, as well as the main collaborators involved.
                </li>
                <li>
                  Provide to the community an intuitive and customizable impact evaluation
                  tool to capture process and results outcomes in a harmonized manner
                </li>
              </ul>
            </v-flex>
            <v-flex md3>
              <v-img src="/img/branding/inspires.png"/>
            </v-flex>
          </v-layout>

          <p>
            In the end, we hope that the platform will support the community (structure
            coordinators and project’s participants around the world) mutual learning by sharing
            science Shops experiences and other participatory research and innovation projects
            good but also failed practices, methodologies, etc.
          </p>

          <h2 class="mb-2">The team behind InSPIRES</h2>

          <p>TODO...</p>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: "About",
  metaInfo: {
    title: "About Us"
  },
  components: {},
  data() {
    return {};
  }
};
</script>
