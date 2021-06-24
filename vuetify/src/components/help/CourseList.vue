<style scoped>
  .flag-icon{
    width: 24px; height:22px; display:inline-block
  }
  .topic-tag{
    position: absolute;
    font-size: 70%;
    font-weight: 700;
    top: 2px;
    right: 4px
  }
  .v-list a{
    text-decoration: none;
    color:inherit;
  }
  a{
    text-decoration: none;
  }
  .headline{
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }
  .line-clamp {
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
  }
</style>

<style>
  .v-list--two-line .v-list__tile{
    height: auto !important;
    min-height: 72px;
  }
</style>

<template>
  <v-layout pa-0 wrap>

    <template v-for="group in groupedCourses">

      <v-flex :key="group.master_id" ma-0 xs12>
        <v-card flat>
          <v-layout pa-0 ma-0>
            <!-- Course Image -->
            <v-flex pa-0 ma-0 sm4 class="hidden-xs-only">
              <v-img :src="group.content.image_url" height="200" />
            </v-flex>
            <!-- Course Summary -->
            <v-flex sm8>
              <v-layout column>
                <v-flex grow pt-2>
                  <v-sheet class="overflow-hidden pa-0" :height="200-50-12">
                    <h3 class="headline mb-2" style="line-height:200%">
                      <router-link :to="group.content.link">
                        <span style="display: inline-block;position: relative;top: 3px;">
                          <v-icon large color="primary">
                            circle
                          </v-icon>
                          <v-icon color="white" style="position:absolute; left:5px; top:6px">mdi-school</v-icon>
                        </span>
                        {{ group.content.title }}
                      </router-link>
                    </h3>
                    <hr class="grey lighten-2 my-2" style="border-width:2px">
                    <div class="line-clamp" style="line-height: 180%">
                      {{ group.content.summary }}
                    </div>
                  </v-sheet>
                </v-flex>
                <!-- Flag row -->
                <v-flex shrink pt-0 class="text-xs-right hidden-xs-only">
                  <router-link
                    v-for="other in group.others"
                    :key="other.id"
                    :to="other.link"
                    class="px-1"
                  >
                    <flag
                      :iso="getFlagIso(other.locale)"
                      :squared="false"
                      style="width: 32px"
                    />
                  </router-link>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>

      <!--
      <v-list-tile :key="group.master_id">
        <v-list-tile-avatar>
          <v-icon>mdi-school</v-icon>
        </v-list-tile-avatar>

        <v-list-tile-content>
          <div class="hidden-sm-and-up text-uppercase topic-tag">
            {{ group.content.topic }}
          </div>
          <v-list-tile-title>
            <strong>
              <router-link :to="group.content.link">
                {{ group.content.title }}
              </router-link>
            </strong>
          </v-list-tile-title>
          <v-list-tile-sub-title>
            {{ group.content.summary }}
          </v-list-tile-sub-title>
        </v-list-tile-content>

        <v-list-tile-action v-if="flags" class="hidden-sm-and-down">
          <v-layout ml-2 row wrap style="max-width:Calc(34px*5); margin: 0px -12px">
            <v-flex v-for="other in group.others.sort()" :key="other.id" shrink pa-1 class="text-xs-center">
              <router-link :to="other.link">
                <flag
                  :iso="getFlagIso(other.locale)"
                  :squared="false"
                />
              </router-link>
            </v-flex>
          </v-layout>
        </v-list-tile-action>
      </v-list-tile>
      -->


    </template>
  </v-layout>
</template>

<script>
import { getFlagIso } from "@/plugins/i18n"

const unique = (value, index, self) => {
  return self.indexOf(value) === index
}

export default {
    props: ['courses', 'flags'],

    data() {
        return {
            getFlagIso
        }
    },

    computed: {

      groupedCourses(){
        let userLang = this.$store.getters['preferences/lang'];
        let masters = this.courses.map(a => a.master).filter(unique).sort();

        // Quick exit while loading
        if(masters.length == 0) return [];

        let grouped = masters.map(m => {
          // contents from the same master, sorted by locale
          let masterContents = this.courses.filter(a => a.master == m).sort((a,b) => a.locale.localeCompare(b.locale))

          let userContent
          // Decide the content we show to the user, if we can match the user's language, shwo that one, otherwise, find the english one.
          try {
            userContent = masterContents.filter(a => a.locale == userLang)[0]
          } catch (error) {
            userContent = masterContents.filter(a => a.locale == 'en')[0]
          }

          return {
            master_id: m,
            content: userContent || masterContents[0],
            others: masterContents
          }
        })

        // Sort by master-inheritet property `sorting`
        grouped.sort((a,b) => a.content.sorting - b.content.sorting )

        // Dividers on topic change and Topic Headers
        grouped[0].header = true
        for(let i = 0; i < grouped.length-1; i++){
          if(grouped[i].content.topic != grouped[i+1].content.topic){
            grouped[i].spaceAfter = true;
            grouped[i+1].header = true;
          }
        }

        return grouped
      }
    },
}
</script>
