<style>
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
</style>


<template>
  <v-layout v-if="project" row wrap align-content-start>
    <v-flex v-if="canManage" pa-0 xs12 class="text-xs-right">
      <v-btn flat outline color="warning" :to="manageLink">
        <v-icon left>edit</v-icon>Manage this Project
      </v-btn>
    </v-flex>

    <!-- Unapproved Project Alert -->
    <v-flex v-if="!isApprovedProject" xs12>
      <v-alert color="info" :value="true" class="title">
        <v-icon dark left>info</v-icon>This project is not approved yet, it will not show up in public lists.
      </v-alert>
    </v-flex>

    <!-- About Sidebar -->
    <v-flex sm4 xs12 class="_no-hidden-xs-only">
      <v-card flat>
        <v-toolbar dense flat color="primary" dark>
          <h1 class="title">{{ $t('pages.projectDetail.about') }}</h1>
        </v-toolbar>
        <v-card-text class="subheading">
          <table>
            <!-- Structure -->
            <template v-if="structure.id">
              <tr>
                <th>{{ $t('noums.structure') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <router-link :to="structure.link">{{ structure.name }}</router-link>
                </td>
              </tr>
            </template>
            <!-- Contact Website -->
            <template v-if="project.contact_website">
              <tr>
                <th>{{ $t('forms.fields.contactWebsite') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="project.contact_website">{{ project.contact_website }}</a>
                </td>
              </tr>
            </template>
            <!-- Contact Email -->
            <template v-if="project.contact_email">
              <tr>
                <th>{{ $t('forms.fields.email') }}:</th>
              </tr>
              <tr>
                <td colspan="2">
                  <a :href="'mailto:'+project.contact_email">{{ project.contact_email }}</a>
                </td>
              </tr>
            </template>

            <!-- Participants -->
            <tr v-if="project.participants.length > 0">
              <th colspan="2" style="text-align:left">{{ $t('forms.fields.participants') }}:</th>
            </tr>
            <tr>
              <td colspan="2">
                <!-- Chip for each participant -->
                <!-- <router-link
                  v-for="part in project.participants"
                  :key="part.id"
                  :to="user(part.user).link"
                >
                  <v-chip>
                    <v-avatar>
                      <img :src="user(part.user).avatar_url">
                    </v-avatar>
                    {{ user(part.user).full_name }} ({{ role(part.role).name }})
                  </v-chip>
                </router-link> -->

                <v-parallax
                  :src="roleBg(part.role)"
                  height="32"
                  class="my-2 text-truncate"
                  v-for="part in project.participants"
                  :key="part.id">
                  {{ user(part.user).full_name }} ({{ role(part.role).name }})
                </v-parallax>

              </td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </v-flex>

    <v-flex xs12 sm8>
      <v-card flat>
        <v-img :src="project.image_url" height="200">
          <v-toolbar flat style="background-color:rgba(0,0,0,.3)" dark>
            <h1 class="title">{{ project.name }}</h1>
          </v-toolbar>
        </v-img>

        <div class="px-4 pt-4 pb-2 grey lighten-4" style="font-spacing:110%">
          <vue-markdown>{{ project.summary }}</vue-markdown>
        </div>

        <v-card-text>
          <vue-markdown>{{ project.description }}</vue-markdown>
        </v-card-text>

      </v-card>
    </v-flex>

    <v-flex xs12 md-8>
      <v-card flat>
        <v-card-text>
          <h2 class="headline mb-4">Related projects</h2>

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
      project: null
    };
  },

  computed: {
    projectId() {
      return slug2id(this.$route.params.slug);
    },
    structure() {
      return this.$store.getters['structure/detail'](this.project.collaboration.structure);
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
    }
  },

  async created() {
    try {
      this.$store.dispatch("project/load");
      await this.$store.dispatch("project/load", [this.projectId]);
      this.project = this.$store.getters["project/detail"](this.projectId);
      this.$store.dispatch("structure/load", [this.project.collaboration.structure]);
    } catch (err) {
      // TODO: Show error instead
      this.$router.push("/project-not-found");
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
