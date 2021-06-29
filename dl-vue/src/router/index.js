import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(), // hash模式：createWebHashHistory，history模式：createWebHistory
  routes: [
    {
      path: '/',
      redirect: '/Home'
    },
    {
      path: '/Home',
      name: 'Home',
      component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
    },
    {
      path: '/Live',
      name: 'Live',
      component: () => import(/* webpackChunkName: "live" */ '../views/Live.vue')
    },
    {
      path: '/DL',
      name: 'DL',
      component: () => import(/* webpackChunkName: "dl" */ '../views/DL.vue')
    },
  ]
})

export default router