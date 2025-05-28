<template>
    <div class="card">
      <div class="card-body">
        <h2>Журнал успеваемости</h2>
        <div class="controls mb-3">
          <button @click="generateJournal" class="btn btn-primary">Сформировать журнал</button>
        </div>
        <div v-if="selectedStudent" class="student-info mb-3 p-3">
          <h3>{{ selectedStudent.full_name }}</h3>
          <p>Класс: {{ selectedStudent.grade }}</p>
          <p>Цель: {{ selectedStudent.learning_goal.name }}</p>
          <p>Категория: {{ selectedStudent.learning_category.name }}</p>
          <p>Преподаватель: {{ selectedStudent.teacher.full_name }}</p>
          <div class="journal-form p-3" v-if="showJournalForm">
            <div class="form-group mb-3">
              <label>Количество уроков для анализа:</label>
              <select v-model="lessonsCount" class="form-select">
                <option value="3">3</option>
                <option value="5">5</option>
                <option value="10">10</option>
              </select>
            </div>
            <button @click="createJournalEntry" class="btn btn-primary">Создать запись в журнале</button>
          </div>
        </div>
        <div v-for="entry in filteredJournalEntries" :key="entry.id" class="journal-entry mb-3 p-3">
          <h3>Запись от {{ formatDate(entry.created_at) }}</h3>
          <div class="section">
            <h4>Результаты:</h4>
            <p>{{ entry.good_results }}</p>
            <p>{{ entry.bad_results }}</p>
          </div>
          <div class="section">
            <h4>Пройденные темы:</h4>
            <p>{{ entry.covered_topics }}</p>
          </div>
          <div class="section">
            <h4>Работаем над:</h4>
            <p>{{ entry.working_on }}</p>
          </div>
          <div class="section">
            <h4>Рекомендуемый объем занятий:</h4>
            <p>{{ entry.recommended_lessons }} занятий</p>
            <p>{{ entry.recommendation_reason }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    name: 'JournalManagement',
    props: {
      studentId: {
        type: Number,
        required: true,
      },
    },
    setup(props) {
      const journalEntries = ref([]);
      const students = ref([]);
      const selectedStudent = ref(null);
      const showJournalForm = ref(false);
      const lessonsCount = ref(5);
  
      const fetchJournalEntries = async () => {
        try {
          const response = await axios.get(`/api/journal/?student=${props.studentId}`);
          journalEntries.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке журнала:', error);
        }
      };
  
      const fetchStudents = async () => {
        try {
          const response = await axios.get(`/api/students/${props.studentId}/`);
          students.value = [response.data];
          selectedStudent.value = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке учеников:', error);
        }
      };
  
      const generateJournal = () => {
        showJournalForm.value = true;
      };
  
      const createJournalEntry = async () => {
        try {
          await axios.post('/api/journal/generate/', {
            student_id: props.studentId,
            lessons_count: lessonsCount.value,
          });
          await fetchJournalEntries();
          showJournalForm.value = false;
        } catch (error) {
          console.error('Ошибка при создании записи в журнале:', error);
        }
      };
  
      const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString();
      };
  
      const filteredJournalEntries = computed(() => {
        return journalEntries.value.filter((entry) => entry.student.id == props.studentId);
      });
  
      onMounted(() => {
        fetchJournalEntries();
        fetchStudents();
      });
  
      return {
        journalEntries,
        students,
        selectedStudent,
        showJournalForm,
        lessonsCount,
        generateJournal,
        createJournalEntry,
        formatDate,
        filteredJournalEntries,
      };
    },
  };
  </script>
  
  <style scoped>
  .controls {
    margin-bottom: 20px;
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
  
  .section {
    margin-bottom: 15px;
  }
  
  .section h4 {
    margin-bottom: 5px;
    color: #444;
  }
  </style>