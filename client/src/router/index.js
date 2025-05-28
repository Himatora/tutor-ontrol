import { createRouter, createWebHistory } from 'vue-router';
import Home from "../views/Home.vue";
import CategoryPage from "../views/CategoryPage.vue";
import StudentLessons from "../views/StudentLessons.vue";

const routes = [
  { path: '/', component: Home },
  { path: '/:category', component: CategoryPage },
  { path: '/:category/:studentId', component: StudentLessons },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;