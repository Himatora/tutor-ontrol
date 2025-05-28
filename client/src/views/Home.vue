<template>
  <div>
    <h1 class="mb-4 text-primary">Система учета занятий</h1>
    <nav class="navbar navbar-expand-lg navbar-dark mb-4">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li v-for="category in categories" :key="category.id" class="nav-item">
              <router-link class="nav-link" :to="'/' + category.slug">{{ category.name }}</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="row">
      <div v-for="category in categories" :key="category.id" class="col-md-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <h3>{{ category.name }}</h3>
            <p>Подготовка к {{ category.name }}</p>
            <router-link :to="'/' + category.slug" class="btn btn-primary">Перейти</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      categories: [],
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('/api/learning-categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке категорий:', error);
      }
    },
  },
};
</script>