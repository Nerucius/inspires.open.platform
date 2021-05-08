<style scoped>
  .container .v-list a{ text-decoration: none; }
  .container .v-list a:hover{ text-decoration: underline; }
</style>


<template>
  <v-layout v-if="authorized" row wrap align-content-start>
    <v-flex xs12>
      <h1>{{ $t('pages.admin.mainTitle') }}</h1>
    </v-flex>

    <v-flex xs12>
      <ManageNetworks />
    </v-flex>

    <!-- Pending structures -->
    <v-flex xs12>
      <PendingStructures @change="refreshStructures" />
    </v-flex>

    <!-- Validated structures -->
    <v-flex xs12>
      <ValidatedStructures @change="refreshStructures" />
    </v-flex>

    <v-flex xs12>
      <DataExport />
    </v-flex>
  </v-layout>

  <!-- Alert for unauthorized -->
  <v-layout v-else>
    <v-flex xs12>
      <v-alert color="error" :value="true" class="headline">
        <v-layout row align-center>
          <v-flex>
            <v-icon large dark>
              warning
            </v-icon>
          </v-flex>
          <v-flex>
            {{ $t('pages.admin.unauthorizedAccess') }}
          </v-flex>
        </v-layout>
      </v-alert>
    </v-flex>
  </v-layout>
</template>

<script>
import DataExport from "@/components/admin/DataExport";
import PendingStructures from "@/components/admin/PendingStructures";
import ValidatedStructures from "@/components/admin/ValidatedStructures";
import ManageNetworks from "@/components/admin/ManageNetworks";

export default {

  metaInfo(){
    return {
      title: this.$t("pages.admin.mainTitle")
    }
  },

  components:{
    DataExport,
    PendingStructures,
    ValidatedStructures,
    ManageNetworks,
  },


  data(){
    return{
      rules: {
        required: v => !!v || this.$t("forms.rules.requiredField"),
        minlen: v =>
          v.length > 10 || this.$t("forms.rules.minimunLength", { length: 10 })
      },
    }
  },

  computed:{
    user(){
      return this.$store.getters['user/current']
    },
    authorized(){
      return this.user.is_administrator
    },
  },


  created(){
    this.refreshStructures()
  },

  methods:{
    refreshStructures(){
      this.$store.dispatch("structure/clear")
      // Load all structures
      this.$store.dispatch("structure/load", )
      this.$store.dispatch("structure/load", {params:{nonvalidated:true}})
    },
  },


};
</script>
