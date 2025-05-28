<template>
    <div class="card mb-4">
      <div class="card-body">
        <h2>Управление уроками</h2>
        <div class="form-section mb-4">
          <h3>Добавить урок</h3>
          <div class="form-group mb-3">
            <label>Вид урока:</label>
            <select v-model="newLesson.lesson_type" class="form-select">
              <option v-for="type in lessonTypes" :value="type.id">{{ type.name }}</option>
            </select>
          </div>
          <div class="form-group mb-3">
            <label>Тема:</label>
            <div class="input-group">
              <select v-model="newLesson.topic" class="form-select">
                <option v-for="topic in topics" :value="topic.id">{{ topic.name }}</option>
              </select>
              <button @click="showAddTopicModal = true" class="btn btn-outline-secondary">+</button>
            </div>
          </div>
          <div class="form-group mb-3">
            <label>Комментарий:</label>
            <textarea v-model="newLesson.comment" class="form-control"></textarea>
          </div>
          <button @click="addLesson" class="btn btn-primary">Добавить урок</button>
        </div>
  
        <div class="list-section">
          <h3>Список уроков</h3>
          <div class="filters mb-3">
            <select v-model="typeFilter" class="form-select w-auto">
              <option value="">Все виды</option>
              <option v-for="type in lessonTypes" :value="type.id">{{ type.name }}</option>
            </select>
          </div>
          <div v-for="lesson in filteredLessons" :key="lesson.id" class="lesson-card mb-3 p-3">
            <h4>{{ lesson.student.full_name }}</h4>
            <p><strong>Тип:</strong> {{ lesson.lesson_type.name }}</p>
            <p><strong>Тема:</strong> {{ lesson.topic.name }}</p>
            <p><strong>Дата:</strong> {{ formatDate(lesson.date) }}</p>
            <p><strong>Комментарий:</strong> {{ lesson.comment || 'нет' }}</p>
            <button @click="addHomework(lesson)" class="btn btn-primary">Добавить ДЗ</button>
          </div>
        </div>
  
        <div v-if="showAddTopicModal" class="modal fade show d-block" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h3 class="modal-title">Добавить новую тему</h3>
                <button type="button" class="btn-close" @click="showAddTopicModal = false"></button>
              </div>
              <div class="modal-body">
                <input v-model="newTopicName" type="text" class="form-control" placeholder="Название темы" />
              </div>
              <div class="modal-footer">
                <button @click="addTopic" class="btn btn-primary">Добавить</button>
                <button @click="showAddTopicModal = false" class="btn btn-outline-secondary">Отмена</button>
              </div>
            </div>
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
  
  export default {
    name: 'LessonManagement',
    props: {
      studentId: {
        type: Number,
        required: true,
      },
    },
    setup(props) {
      const lessons = ref([]);
      const students = ref([]);
      const lessonTypes = ref([]);
      const topics = ref([]);
      const typeFilter = ref('');
      const showAddTopicModal = ref(false);
      const showAddHomeworkModal = ref(false);
      const newTopicName = ref('');
      const selectedLesson = ref(null);
      const newLesson = ref({
        student: props.studentId,
        lesson_type: 2,
        topic: null,
        comment: '',
      });
      const newHomework = ref({
        lesson: null,
        topics: [],
        status: 'ASSIGNED',
        difficulty: 'MEDIUM',
        result: null,
      });
  
      const fetchLessons = async () => {
        try {
          const response = await axios.get(`/api/lessons/?student=${props.studentId}`);
          lessons.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке уроков:', error);
        }
      };
  
      const fetchStudents = async () => {
        try {
          const response = await axios.get(`/api/students/${props.studentId}/`);
          students.value = [response.data];
        } catch (error) {
          console.error('Ошибка при загрузке учеников:', error);
        }
      };
  
      const fetchLessonTypes = async () => {
        try {
          const response = await axios.get('/api/lesson-types/');
          lessonTypes.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке видов уроков:', error);
        }
      };
  
      const fetchTopics = async () => {
        try {
          const response = await axios.get('/api/topics/');
          topics.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке тем:', error);
        }
      };
  
      const addLesson = async () => {
        try {
          await axios.post('/api/lessons/', {
            student: newLesson.value.student,
            lesson_type: newLesson.value.lesson_type,
            topic: newLesson.value.topic,
            comment: newLesson.value.comment,
          });
          await fetchLessons();
          newLesson.value = {
            student: props.studentId,
            lesson_type: null,
            topic: null,
            comment: '',
          };
        } catch (error) {
          console.error('Ошибка при добавлении урока:', error);
        }
      };
  
      const addTopic = async () => {
        try {
          await axios.post('/api/topics/', { name: newTopicName.value });
          await fetchTopics();
          newTopicName.value = '';
          showAddTopicModal.value = false;
        } catch (error) {
          console.error('Ошибка при добавлении темы:', error);
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
          await axios.post('/api/homework/', newHomework.value);
          showAddHomeworkModal.value = false;
          await fetchLessons();
        } catch (error) {
          console.error('Ошибка при сохранении ДЗ:', error);
        }
      };
  
      const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
      };
  
      const filteredLessons = computed(() => {
        let result = lessons.value;
        if (typeFilter.value) {
          result = result.filter((lesson) => lesson.lesson_type.id == typeFilter.value);
        }
        return result;
      });
  
      onMounted(() => {
        fetchLessons();
        fetchStudents();
        fetchLessonTypes();
        fetchTopics();
      });
  
      return {
        lessons,
        students,
        lessonTypes,
        topics,
        newLesson,
        newTopicName,
        newHomework,
        showAddTopicModal,
        showAddHomeworkModal,
        typeFilter,
        addLesson,
        addTopic,
        addHomework,
        saveHomework,
        formatDate,
        filteredLessons,
      };
    },
  };
  </script>
  
  <style scoped>
  .form-section,
  .list-section {
    margin-bottom: 30px;
    padding: 15px;
    border: 1px solid var(--bs-secondary);
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .filters {
    margin-bottom: 15px;
    display: flex;
    gap: 10px;
  }
  </style>