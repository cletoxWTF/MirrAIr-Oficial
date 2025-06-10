import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import BenchmarkView from '../views/BenchmarkView.vue'
import MetricsView from '../views/MetricsView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/benchmark',
    name: 'benchmark',
    component: BenchmarkView
  },
  {
    path: '/metrics',
    name: 'metrics',
    component: MetricsView
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
