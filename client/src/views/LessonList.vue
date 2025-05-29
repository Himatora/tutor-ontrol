<template>
    <div class="card mb-4">
      <div class="card-body">
        <h2>Список уроков</h2>
        <div>
    <nav class="navbar navbar-expand-lg navbar-dark mb-4">
      <div class="container-fluid">
        <router-link :to="`/${categorySlug}`" class="navbar-brand">Назад</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
      <div class="collapse navbar-collapse" id="navbarNav">
      <div class="navbar-nav">
          <a class="nav-link active" href="#">Просмотреть уроки</a>
          <router-link :to="`/${categorySlug}/${$route.params.studentId}`" class="nav-link">Уроки и журнал</router-link>
          
        </div>
      </div>
    </nav>
  </div>
        <div class="filters mb-3 d-flex gap-3">
          <select v-model="typeFilter" class="form-select w-auto">
            <option value="">Все виды</option>
            <option v-for="type in lessonTypes" :value="type.id">{{ type.name }}</option>
          </select>
          <input v-model="dateFilter" type="date" class="form-control w-auto" />
          <button @click="resetFilters" class="btn btn-outline-secondary">Сбросить</button>
        </div>
        <div v-if="isLoading" class="text-center my-4">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Загрузка...</span>
          </div>
        </div>
        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        <div v-else>
          <div v-for="lesson in filteredLessons" :key="lesson.id" class="lesson-card mb-3 p-3 border rounded">
            <p><strong>Тип:</strong> {{ lesson.lesson_type.name }}</p>
            <p><strong>Тема:</strong> {{ lesson.topic.name }}</p>
            <p><strong>Дата:</strong> {{ formatDate(lesson.date) }}</p>
            <p><strong>Комментарий:</strong> {{ lesson.comment || 'нет' }}</p>
            <button @click="addHomework(lesson)" class="btn btn-primary">Добавить ДЗ</button>
          </div>
          <div v-if="filteredLessons.length === 0" class="text-center text-muted py-4">
            Уроки не найдены. Попробуйте изменить фильтры.
          </div>
        </div>
  
        <div v-if="showAddHomeworkModal" class="modal fade show d-block" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h3 class="modal-title">Добавить домашнее задание</h3>
                <button type="button" class="btn-close" @click="showAddHomeworkModal = false"></button>
              </div>
              <div class="modal-body">
                <div class="form-group mb-3">
                  <label>Темы:</label>
                  <div v-for="topic in topics" :key="topic.id" class="form-check">
                    <input type="checkbox" v-model="newHomework.topics" :value="topic.id" class="form-check-input" />
                    <label class="form-check-label">{{ topic.name }}</label>
                  </div>
                </div>
                <div class="form-group mb-3">
                  <label>Состояние:</label>
                  <select v-model="newHomework.status" class="form-select">
                    <option value="ASSIGNED">Задано</option>
                    <option value="NOT_ASSIGNED">Не задано</option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label>Категория заданий:</label>
                  <select v-model="newHomework.difficulty" class="form-select">
                    <option value="EASY">Легкий</option>
                    <option value="MEDIUM">Средний</option>
                    <option value="HARD">Сложный</option>
                  </select>
                </div>
                <div class="form-group mb-3">
                  <label>Результат (% выполнения):</label>
                  <input v-model="newHomework.result" type="number" min="0" max="100" class="form-control" />
                </div>
              </div>
              <div class="modal-footer">
                <button @click="saveHomework" class="btn btn-primary">Сохранить ДЗ</button>
                <button @click="showAddHomeworkModal = false" class="btn btn-outline-secondary">Отмена</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  
  axios.defaults.baseURL = 'http://localhost:8000';
  
  export default {
    name: 'LessonList',
    props: {
      studentId: {
        type: Number,
        required: true,
      },
    },
    setup(props) {
      const lessons = ref([]);
      const lessonTypes = ref([]);
      const topics = ref([]);
      const typeFilter = ref('');
      const dateFilter = ref('');
      const showAddHomeworkModal = ref(false);
      const selectedLesson = ref(null);
      const newHomework = ref({
        lesson: null,
        topics: [],
        status: 'ASSIGNED',
        difficulty: 'MEDIUM',
        result: null,
      });
      const isLoading = ref(true);
      const error = ref(null);
  
      const fetchLessons = async () => {
        try {
          const response = await axios.get(`/api/lessons/?student=${props.studentId}`);
          console.log('Ответ /api/lessons:', JSON.stringify(response.data, null, 2));
          lessons.value = response.data;
          if (response.data.length === 0) {
            error.value = 'Уроки не найдены для этого ученика.';
          }
        } catch (error) {
          console.error('Ошибка при загрузке уроков:', error.response?.data || error.message);
          error.value = 'Не удалось загрузить уроки: ' + (error.response?.data?.detail || error.message);
        } finally {
          isLoading.value = false;
        }
      };
  
      const fetchLessonTypes = async () => {
        try {
          const response = await axios.get('/api/lesson-types/');
          lessonTypes.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке видов уроков:', error.response?.data || error.message);
        }
      };
  
      const fetchTopics = async () => {
        try {
          const response = await axios.get('/api/topics/');
          topics.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке тем:', error.response?.data || error.message);
        }
      };
  
      const addHomework = (lesson) => {
        selectedLesson.value = lesson;
        newHomework.value = {
          lesson: lesson.id,
          topics: [],
          status: 'ASSIGNED',
          difficulty: 'MEDIUM',
          result: null,
        };
        showAddHomeworkModal.value = true;
      };
  
      const saveHomework = async () => {
        try {
          const homeworkData = {
            lesson: newHomework.value.lesson,
            topic_ids: newHomework.value.topics,
            status: newHomework.value.status,
            difficulty: newHomework.value.difficulty,
            result: newHomework.value.result ? Number(newHomework.value.result) : null,
          };
          await axios.post('/api/homework/', homeworkData, {
            headers: { 'Content-Type': 'application/json' },
          });
          showAddHomeworkModal.value = false;
          await fetchLessons();
        } catch (error) {
          console.error('Ошибка при сохранении ДЗ:', error.response?.data || error.message);
        }
      };
  
      const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
      };
  
      const resetFilters = () => {
        typeFilter.value = '';
        dateFilter.value = '';
      };
  
      const filteredLessons = computed(() => {
        let result = lessons.value;
        if (typeFilter.value) {
          result = result.filter((lesson) => lesson.lesson_type.id == typeFilter.value);
        }
        if (dateFilter.value) {
          const filterDate = new Date(dateFilter.value).toISOString().split('T')[0];
          result = result.filter((lesson) => lesson.date.includes(filterDate));
        }
        return result;
      });
  
      onMounted(() => {
        fetchLessons();
        fetchLessonTypes();
        fetchTopics();
      });
  
      return {
        lessons,
        lessonTypes,
        topics,
        typeFilter,
        dateFilter,
        showAddHomeworkModal,
        newHomework,
        isLoading,
        error,
        addHomework,
        saveHomework,
        formatDate,
        filteredLessons,
        resetFilters,
      };
    },
  };
  </script>
  
  <style scoped>
  .lesson-card {
    border: 1px solid var(--bs-secondary);
    border-radius: 5px;
  }
  .filters {
    display: flex;
    gap: 10px;
  }
  .form-group {
    margin-bottom: 15px;
  }
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  </style>