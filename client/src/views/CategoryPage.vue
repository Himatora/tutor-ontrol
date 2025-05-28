<template>
  <div>
    <h1 v-if="category" class="mb-4 text-primary">{{ category.name }} - Управление учениками</h1>
    <h1 v-else class="mb-4 text-primary">Загрузка...</h1>
    <nav class="navbar navbar-expand-lg navbar-dark mb-4">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Назад</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link :to="`/${$route.params.category}`" class="nav-link active">Ученики</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <StudentManagement v-if="category" :category-slug="$route.params.category" :category-id="category.id" :category-name="category.name" />
    <div v-else class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import StudentManagement from '../components/StudentManagement.vue';

export default {
  name: 'CategoryPage',
  components: { StudentManagement },
  data() {
    return {
      category: null,
    };
  },
  async mounted() {
    await this.fetchCategory();
  },
  methods: {
    async fetchCategory() {
      try {
        const slug = this.$route.params.category;
        console.log('Запрос категории с slug:', slug);
        const response = await axios.get(`/api/learning-categories/?slug=${slug}`);
        console.log('Ответ API:', response.data);
        if (response.data.id) {
          this.category = response.data;
        } else {
          console.error('Категория не найдена для slug:', slug);
          this.$router.push('/');
        }
      } catch (error) {
        console.error('Ошибка при загрузке категории:', error);
        this.$router.push('/');
      }
    },
  },
};
</script>