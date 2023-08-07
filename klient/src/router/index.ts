import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(savedPosition)
        }, 500)
      })
    }
    if (to.hash) {
      if (to.name === from.name) {
        return { el: to.hash, behavior: 'smooth' };
      }
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve({ el: to.hash, behavior: 'smooth' })
        }, 500)
      })
    }

    return { top: 0 };
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/wiki',
      name: 'wikiMain',
      component: () => import('../views/WikiView.vue')
    },
    {
      path: '/input',
      name: 'statementsInput',
      component: () => import('../views/StatementsView.vue'),
      props: true
    },
    {
      path: '/cnf',
      name: 'cnf',
      component: () => import('../views/ClausalView.vue'),
      props: true
    },
    {
      path: '/solution',
      name: 'solution',
      component: () => import('../views/SolutionView.vue'),
      props: true
    },
    {
      path: '/graph',
      name: 'graph',
      component: () => import('../views/TreeView.vue'),
    },
  ],
})

export default router
