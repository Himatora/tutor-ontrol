<template>
    <div>
      <h1 class="mb-4 text-primary">{{ categoryName }} - Ученик: {{ student?.full_name }}</h1>
      <nav class="navbar navbar-expand-lg navbar-dark mb-4">
        <div class="container-fluid">
          <router-link :to="`/${$route.params.category}`" class="navbar-brand">Назад</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link active" href="#">Уроки и журнал</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <div class="row">
        <div class="col-md-6">
          <LessonManagement :studentId="parseInt($route.params.studentId)" />
        </div>
        <div class="col-md-6">
          <JournalManagement :studentId="parseInt($route.params.studentId)" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import LessonManagement from "../components/LessonManagement.vue";
  import JournalManagement from "../components/JournalManagement.vue";
  import axios from 'axios';
  
  export default {
    name: 'StudentLessons',
    components: { LessonManagement, JournalManagement },
    data() {
      return {
        student: null,
      };
    },
    computed: {
      categoryName() {
        const category = this.$route.params.category;
        return category === 'ege' ? 'ЕГЭ' : category === 'oge' ? 'ОГЭ' : 'Универсальная';
      },
    },
    async created() {
      try {
        const response = await axios.get(`/api/students/${this.$route.params.studentId}/`);
        this.student = response.data;
      } catch (error) {
        console.error('Ошибка загрузки данных ученика:', error);
      }
    },
  };
  </script>