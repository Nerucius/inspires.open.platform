<template>
  <v-card flat>
    <v-card-title>
      <h2 class="title">
        {{ $t("pages.admin.pendingApproval") }}
      </h2>
    </v-card-title>
    <v-card-text>
      <p class="subheading"><vue-markdown>{{ $t("pages.admin.instructionsText") }}</vue-markdown></p>

      <v-list two-line>
        <template v-for="(structure, idx) in structuresPending">
          <v-list-tile :key="structure.id">
            <!-- Structure Image -->
            <v-list-tile-avatar>
              <!-- <img :src="getUser(structure.created_by).avatar_url"> -->
              <img :src="structure.image_url" />
            </v-list-tile-avatar>

            <!-- Tile content -->
            <v-list-tile-content>
              <v-list-tile-title>
                <router-link :to="structure.link">
                  <strong>
                    {{ structure.name }}
                  </strong>
                </router-link>
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <router-link :to="getUser(structure.created_by).link">
                  {{
                    $t("pages.admin.createdBy", {
                      name: getUser(structure.created_by).full_name,
                    })
                  }}
                </router-link>
              </v-list-tile-sub-title>
            </v-list-tile-content>

            <v-list-tile-action>
              <v-btn
                color="success"
                class="elevation-0"
                @click="validate(structure.id)"
              >
                Validate
              </v-btn>
            </v-list-tile-action>
          </v-list-tile>

          <v-divider
            v-if="idx != structuresPending.length - 1"
            :key="`div-${structure.id}`"
            inset
          />
        </template>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {

  computed:{
    structuresPending(){
      return this.$store.getters['structure/all'].filter(s => !s.is_valid)
    },
  },

  methods: {
    getUser(id){
      return this.$store.getters['user/get'](id)
    },

    async validate(structureId){
      if (!confirm('Are you sure you want to validate this structure?')) return;

      try{
        await this.$store.dispatch("structure/validate", structureId);
        this.$store.dispatch("toast/success", this.$t("pages.admin.validationSuccess"))

      }catch(error){
        this.$store.dispatch("toast/error", {
          message: this.$t("pages.admin.validationFailure"),
          error
        })
      }
      
      this.$emit('change')
    },
  },

};
</script>
