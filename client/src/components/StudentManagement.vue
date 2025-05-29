<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Список учеников</h2>
      <button @click="showAddModal" class="btn btn-primary">
        <i class="bi bi-plus-lg me-1"></i> Добавить ученика
      </button>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input v-model="searchQuery" placeholder="Поиск по ФИО" class="form-control" />
          </div>
          <div class="col-md-3">
            <select v-model="gradeFilter" class="form-select">
              <option value="">Все классы</option>
              <option v-for="grade in 11" :value="grade">{{ grade }} класс</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="categoryFilter" class="form-select" disabled>
              <option :value="categoryId">{{ categoryName }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <button @click="resetFilters" class="btn btn-outline-secondary w-100">Сбросить</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else class="card">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead>
              <tr>
                <th @click="sortBy('full_name')" class="cursor-pointer">
                  ФИО <i class="bi bi-arrow-down-up ms-1"></i>
                </th>
                <th @click="sortBy('grade')" class="cursor-pointer">
                  Класс <i class="bi bi-arrow-down-up ms-1"></i>
                </th>
                <th>Цель</th>
                <th>Преподаватель</th>
                <th class="text-end">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id" @click="goToLessons(student.id)">
                <td>{{ student.full_name }}</td>
                <td>{{ student.grade }} класс</td>
                <td>{{ student.learning_goal.name }}</td>
                <td>{{ student.teacher.full_name }}</td>
                <td class="text-end">
                  <button @click.stop="editStudent(student)" class="btn btn-sm btn-outline-primary me-2" title="Редактировать">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button @click.stop="confirmDelete(student.id)" class="btn btn-sm btn-outline-danger" title="Удалить">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredStudents.length === 0">
                <td colspan="5" class="text-center text-muted py-4">
                  Ничего не найдено. Попробуйте изменить параметры поиска или добавить учеников.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Модальное окно ученика -->
    <div class="modal fade" id="studentModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingStudent ? 'Редактирование ученика' : 'Новый ученик' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveStudent">
              <div class="mb-3">
                <label class="form-label">ФИО *</label>
                <input v-model="studentForm.full_name" type="text" class="form-control" required />
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label">Класс *</label>
                  <select v-model="studentForm.grade" class="form-select" required>
                    <option v-for="grade in 11" :value="grade">{{ grade }} класс</option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Преподаватель *</label>
                  <select v-model="studentForm.teacher" class="form-select" required>
                    <option v-for="teacher in teachers" :value="teacher.id">{{ teacher.full_name }} ({{ teacher.subject }})</option>
                  </select>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label class="form-label">Цель обучения *</label>
                  <div class="input-group">
                    <select v-model="studentForm.learning_goal" class="form-select" required>
                      <option v-for="goal in goals" :value="goal.id">{{ goal.name }}</option>
                    </select>
                    <button @click="showGoalModal" type="button" class="btn btn-outline-secondary">
                      <i class="bi bi-plus"></i>
                    </button>
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Категория *</label>
                  <select v-model="studentForm.learning_category" class="form-select" required disabled>
                    <option :value="categoryId">{{ categoryName }}</option>
                  </select>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="submit" class="btn btn-primary">{{ editingStudent ? 'Сохранить' : 'Добавить' }}</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно цели -->
    <div class="modal fade" id="goalModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h6 class="modal-title">Новая цель обучения</h6>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Название *</label>
              <input v-model="newGoalName" type="text" class="form-control" placeholder="Например: Подготовка к ОГЭ" required />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-primary" @click="addGoal" :disabled="!newGoalName">Добавить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <div class="modal fade" id="deleteModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">Подтверждение удаления</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Вы действительно хотите удалить этого ученика? Все связанные данные также будут удалены.
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Отмена</button>
            <button type="button" class="btn btn-danger" @click="deleteStudent">Удалить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { Modal } from 'bootstrap';

// Устанавливаем базовый URL
axios.defaults.baseURL = 'http://localhost:8000';

export default {
  name: 'StudentManagement',
  props: {
    categorySlug: { type: String, required: true },
    categoryId: { type: Number, required: true },
    categoryName: { type: String, required: true },
  },
  setup(props) {
    const router = useRouter();
    const students = ref([]);
    const goals = ref([]);
    const teachers = ref([]);
    const searchQuery = ref('');
    const gradeFilter = ref('');
    const categoryFilter = ref(props.categoryId);
    const sortField = ref('full_name');
    const sortDirection = ref('asc');
    const newGoalName = ref('');
    const editingStudent = ref(null);
    const studentToDelete = ref(null);
    const isLoading = ref(true);
    const error = ref(null);
    const studentForm = ref({
      full_name: '',
      grade: 5,
      learning_goal: null,
      learning_category: props.categoryId,
      teacher: null,
    });

    let studentModal = null;
    let goalModal = null;
    let deleteModal = null;

    const loadData = async () => {
      isLoading.value = true;
      error.value = null;
      try {
        console.log('Fetching data for category ID:', props.categoryId);

        const [studentsRes, goalsRes, teachersRes] = await Promise.all([
          axios.get(`/api/students/?learning_category=${encodeURIComponent(props.categoryId)}`),
          axios.get('/api/learning-goals/'),
          axios.get('/api/teachers/'),
        ]);

        console.log('API /students response:', studentsRes.data);
        console.log('API /learning-goals response:', goalsRes.data);
        console.log('API /teachers response:', teachersRes.data);

        students.value = studentsRes.data;
        goals.value = goalsRes.data;
        teachers.value = teachersRes.data;

        if (goals.value.length > 0) studentForm.value.learning_goal = goals.value[0].id;
        if (teachers.value.length > 0) studentForm.value.teacher = teachers.value[0].id;

        if (students.value.length === 0) {
          error.value = 'Нет учеников для этой категории. Добавьте нового ученика.';
        }
      } catch (err) {
        console.error('General data loading error:', err.response?.data || err.message);
        error.value = 'Не удалось загрузить данные. Попробуйте позже.';
      } finally {
        isLoading.value = false;
      }
    };

    const showAddModal = () => {
      resetForm();
      editingStudent.value = null;
      studentModal.show();
    };

    const showGoalModal = () => {
      newGoalName.value = '';
      studentModal.hide();
      goalModal.show();
    };

    const confirmDelete = (id) => {
      studentToDelete.value = id;
      deleteModal.show();
    };

    const addGoal = async () => {
      if (!newGoalName.value) return;
      try {
        await axios.post('/api/learning-goals/', { name: newGoalName.value }, {
          headers: { 'Content-Type': 'application/json' },
        });
        await loadData();
        goalModal.hide();
        studentModal.show();
      } catch (error) {
        console.error('Ошибка добавления цели:', error.response?.data || error.message);
      }
    };

    const saveStudent = async () => {
      try {
        const data = {
          full_name: studentForm.value.full_name,
          grade: Number(studentForm.value.grade),
          learning_goal_id: Number(studentForm.value.learning_goal),
          learning_category_id: Number(studentForm.value.learning_category),
          teacher_id: Number(studentForm.value.teacher),
        };
        console.log('Отправляемые данные:', data);

        const config = {
          headers: { 'Content-Type': 'application/json' },
        };

        if (editingStudent.value) {
          console.log('PUT запрос на:', `/api/students/${editingStudent.value.id}/`);
          await axios.put(`/api/students/${editingStudent.value.id}/`, data, config);
        } else {
          console.log('POST запрос на:', '/api/students/');
          await axios.post('/api/students/', data, config);
        }
        await loadData();
        studentModal.hide();
      } catch (error) {
        console.error('Ошибка сохранения ученика:', JSON.stringify(error.response?.data, null, 2));
        error.value = 'Не удалось сохранить ученика: ' + (error.response?.data?.detail || error.message);
      }
    };

    const deleteStudent = async () => {
      try {
        await axios.delete(`/api/students/${studentToDelete.value}/`, {
          headers: { 'Content-Type': 'application/json' },
        });
        await loadData();
        deleteModal.hide();
      } catch (error) {
        console.error('Ошибка удаления ученика:', error.response?.data || error.message);
      }
    };

    const editStudent = (student) => {
      editingStudent.value = student;
      studentForm.value = {
        full_name: student.full_name,
        grade: student.grade,
        learning_goal: student.learning_goal.id,
        learning_category: student.learning_category.id,
        teacher: student.teacher.id,
      };
      studentModal.show();
    };

    const goToLessons = (studentId) => {
      router.push(`/${props.categorySlug}/${studentId}`);
    };

    const resetForm = () => {
      studentForm.value = {
        full_name: '',
        grade: 5,
        learning_goal: goals.value.length > 0 ? goals.value[0].id : null,
        learning_category: props.categoryId,
        teacher: teachers.value.length > 0 ? teachers.value[0].id : null,
      };
    };

    const resetFilters = () => {
      searchQuery.value = '';
      gradeFilter.value = '';
      categoryFilter.value = props.categoryId;
    };

    const sortBy = (field) => {
      if (sortField.value === field) {
        sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
      } else {
        sortField.value = field;
        sortDirection.value = 'asc';
      }
    };

    const filteredStudents = computed(() => {
      let result = students.value;
      console.log('Raw students data:', result);

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter((s) => s.full_name.toLowerCase().includes(query));
      }

      if (gradeFilter.value) {
        result = result.filter((s) => s.grade === Number(gradeFilter.value));
      }

      result = result.sort((a, b) => {
        const modifier = sortDirection.value === 'asc' ? 1 : -1;
        const aValue = a[sortField.value];
        const bValue = b[sortField.value];
        if (aValue < bValue) return -1 * modifier;
        if (aValue > bValue) return 1 * modifier;
        return 0;
      });

      console.log('Filtered students:', result);
      return result;
    });

    onMounted(() => {
      const studentModalEl = document.getElementById('studentModal');
      const goalModalEl = document.getElementById('goalModal');
      const deleteModalEl = document.getElementById('deleteModal');
      studentModal = new Modal(studentModalEl, { backdrop: false });
      goalModal = new Modal(goalModalEl, { backdrop: false });
      deleteModal = new Modal(deleteModalEl, { backdrop: false });
      loadData();
    });

    return {
      students,
      goals,
      teachers,
      searchQuery,
      gradeFilter,
      categoryFilter,
      newGoalName,
      editingStudent,
      studentForm,
      filteredStudents,
      categoryId: props.categoryId,
      isLoading,
      error,
      showAddModal,
      showGoalModal,
      confirmDelete,
      addGoal,
      saveStudent,
      deleteStudent,
      editStudent,
      goToLessons,
      resetFilters,
      sortBy,
    };
  },
};
</script>