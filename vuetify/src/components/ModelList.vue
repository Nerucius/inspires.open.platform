<template>
  <v-card>
    <v-card-title primary-title>
      <h3>{{ $t("book.listOfBooks") }}</h3>
    </v-card-title>
    <v-card-text>
      <v-list>
        <!-- list item -->
        <template v-for="item in items">
          <v-list-tile :key="item.url">
            <v-list-tile-content>
              <v-list-tile-title>{{ item.name }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ item.author }}</v-list-tile-sub-title>
            </v-list-tile-content>
            <v-btn small icon color="error" @click="deleteBook(item)">
              <v-icon small>
                delete
              </v-icon>
            </v-btn>
          </v-list-tile>
          <v-divider :key="item.url" />
        </template>
        <!-- /list item -->
      </v-list>

      <br>

      <div v-if="$store.getters['user/isLoggedIn']" class="px-3">
        <h4>{{ $t("book.addBook") }}</h4>

        <v-form ref="form" v-model="valid" @submit.prevent="submitForm()">
          <v-text-field
            v-model="book.name"
            :rules="rules"
            :label="$t('forms.fields.title')"
            required
          />
          <v-text-field
            v-model="book.author"
            :rules="rules"
            :label="$t('forms.fields.author')"
            required
          />
          <br>
          <v-btn type="submit" :disabled="!valid" color="success">
            {{ $t("actions.add") }}
          </v-btn>
        </v-form>
      </div>

      <!-- <form @submit.prevent="saveBook()">
        Title:
        <input type="text" required v-model="book.name" name="name" id="name">
        <br>Author:
        <input type="text" required v-model="book.author" name="author" id="author">
        <br>
        <button type="submit">Save book</button>
      </form>-->
      <br>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "ModelList",
  data: () => {
    return {
      valid: null,
      book: { name: "", author: "" }
    };
  },

  computed: {
    items() {
      return this.$store.getters.books;
    },
    rules() {
      return [v => !!v || this.$t("forms.rules.requiredField")];
    }
  },

  mounted() {
    this.$store.dispatch("loadBooks");
  },

  methods: {
    submitForm() {
      if (this.$refs.form.validate()) {
        this.saveBook();
        this.$refs.form.reset();
      }
    },
    saveBook() {
      this.$store.dispatch("addBook", this.book);
      this.book = { name: "", author: "" };
    },
    deleteBook(book) {
      if (confirm(this.$t("book.removeBookPrompt"))) {
        this.$store.dispatch("deleteBook", book);
      }
    }
  }
};
</script>
