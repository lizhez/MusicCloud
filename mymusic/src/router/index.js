import { createRouter, createWebHistory } from 'vue-router'

import Home from "@/views/Home";
import Main from "@/components/Main.vue";
import MusicSearch from "@/components/MusicSearch.vue";

const routes = [

  {
    path: '/',
    name: 'SearchWeb',
    component: Home,
    children:[
      {
        path: '/',
        name: 'Main',
        component: Main,
      },
      {
        path: '/searching',
        name: 'MusicSearch',
        component: MusicSearch,

      }
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
