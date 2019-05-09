<style scoped>
  table {
    width: 100%;
  }
  table td,
  table th {
    padding: 0 8px 8px 8px;
  }
  table th {
    text-align: left;
  }
  .v-chip__content {
    cursor: pointer !important;
    text-decoration: none !important;
  }

  .person-slab a{
    color: white;
    text-decoration: none;
    text-shadow: 1px 1px 2px #000;
  }

  .v-list__tile__title{
    font-weight: 500;
  }
</style>

<style>
  .v-list__tile__title p{
    margin-bottom: 0px;
  }

  /* Taller list elements */
  .v-list--two-line .v-list__tile{
    height: auto;
    min-height: 72px;
  }
</style>


<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex v-if="canManage" pa-0 xs12 class="text-xs-right">
      <v-btn flat outline color="warning" :to="manageLink">
        <v-icon left>
          edit
        </v-icon>Manage this Project
      </v-btn>
    </v-flex>

    <!-- Unapproved Project Alert -->
    <v-flex v-if="!isApprovedProject" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>
          info
        </v-icon>This project is not approved yet, it will not show up in public lists.
      </v-alert>
    </v-flex>

    <!-- About Sidebar -->
    <v-flex sm4 xs12 class="_no-hidden-xs-only">
      <v-card flat>
        <v-list two-line class="ma-0 pa-0">
          <v-toolbar dense flat color="primary" dark>
            <h1 class="title">
              {{ $t('pages.projectDetail.about') }}
            </h1>
          </v-toolbar>

          <!-- Structure -->
          <v-list-tile v-if="structure" :to="structure.link">
            <v-list-tile-avatar tile>
              <v-img :src="structure.image_url" />
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ structure.name }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('noums.structure') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Website -->
          <v-list-tile v-if="project.contact_website">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="project.contact_website">
                  {{ project.contact_website }}
                </a>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.contactWebsite') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Email -->
          <v-list-tile v-if="project.contact_email">
            <v-list-tile-content>
              <v-list-tile-title>
                <a :href="`mailto:${project.contact_email}`">
                  {{ project.contact_email }}
                </a>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.contactEmail') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <!-- Contact Address -->
          <v-list-tile v-if="project.contact_postal_address">
            <v-list-tile-content>
              <v-list-tile-title style="height:auto">
                <vue-markdown>{{ project.contact_postal_address }}</vue-markdown>
              </v-list-tile-title>
              <v-list-tile-sub-title>{{ $t('forms.fields.postalAddress') }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-toolbar dense flat color="primary" dark class="mt-3">
            <h1 class="title">
              {{ $t('forms.fields.participants') }}
            </h1>
          </v-toolbar>

          <v-sheet :max-height="72*4.5" style="overflow-y:auto;">
            <template v-for="(part, idx) in project.participants">
              <v-list-tile :key="part.id" :to="user(part.user).link">
                <v-list-tile-avatar>
                  <v-img :src="user(part.user).avatar_url" />
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ user(part.user).full_name }}</v-list-tile-title>
                  <v-list-tile-sub-title>
                    {{ $t(role(part.role).name) }}
                  </v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-divider v-if="idx != project.participants.length - 1" :key="`div-${part.id}`" />
            </template>
          </v-sheet>
        </v-list>
      </v-card>
    </v-flex>

    <!-- Main Body -->
    <v-flex xs12 sm8>
      <v-card flat>
        <v-img :src="project.image_url" height="200">
          <v-toolbar flat style="background-color:rgba(0,0,0,.3)" dark>
            <h1 class="title">
              {{ project.name }}
            </h1>
          </v-toolbar>
        </v-img>

        <div class="px-4 pt-4 pb-2 grey lighten-4" style="font-spacing:110%">
          <vue-markdown>{{ project.summary }}</vue-markdown>
        </div>

        <v-card-text>
          <vue-markdown>{{ project.description }}</vue-markdown>

          <br>

          <div v-if="isParticipant" class="text-xs-right">
            <v-btn :to="{...project.link, name:'evaluation-detail'}"
                   outline
            >
              <v-icon left>
                mdi-school
              </v-icon>
              Go to Evaluation
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-flex>

    <!-- Related Projects -->
    <v-flex v-if="project.related_projects.length > 0" xs12 md-8>
      <v-card flat>
        <v-card-text>
          <h2 class="headline mb-4">
            Related projects
          </h2>

          <ProjectCardHorizontal
            v-for="pid in project.related_projects"
            :key="pid"
            :project="getProject(pid)"
          />
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>



<script>
import { slug2id, obj2slug } from "@/plugins/utils";
import ProjectCardHorizontal from "@/components/project/ProjectCardHorizontal";
import VueMarkdown from 'vue-markdown';

export default {
  metaInfo() {
    return {
      title: (this.project || {}).name
    };
  },

  components: {
    ProjectCardHorizontal,
    VueMarkdown
  },

  data() {
    return {
      obj2slug,
      project: null,
      structure: null,
    };
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    isApprovedProject() {
      return (
        this.project.collaboration != null &&
        this.project.collaboration.is_approved
      );
    },
    manageLink() {
      return {
        name: "project-manage",
        params: { slug: obj2slug(this.project) }
      };
    },
    canManage() {
      let userId = this.$store.getters["user/current"].id;
      let isOwner = this.project.owner == userId;
      let isAdmin = this.project.managers.filter(id => id == userId).length > 0;
      return isOwner || isAdmin;
    },
    isParticipant(){
      return true
    }
  },

  async created() {
    try {
      this.$store.dispatch("project/load");
      await this.$store.dispatch("project/load", [this.projectId]);
      this.project = this.$store.getters["project/detail"](this.projectId);

      // If project has a collaboration, load structure
      if(this.project.collaboration){
        let structureId = this.project.collaboration.structure
        this.$store.dispatch("structure/load", [structureId]);
        this.structure = this.$store.getters['structure/detail'](structureId)
      }


    } catch (error) {
      this.$store.dispatch('toast/error', {message:this.$t('pages.projectDetail.projectNotFound'), error})
      console.error(error)
      // TODO: Show error instead
      // this.$router.push("/project-not-found");
    }
  },

  methods: {
    roleBg(roleId){
      return this.$store.getters['evaluation/roles'][roleId].bg
    },

    getProject(pid) {
      return this.$store.getters["project/get"](pid);
    },

    user(uid) {
      return this.$store.getters["user/get"](uid);
    },

    role(rid) {
      return this.$store.getters["evaluation/roles"][rid];
    }
  }
};
</script>
