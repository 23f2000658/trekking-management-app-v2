import { createRouter, createWebHistory } from 'vue-router'

import LandingPage from '../views/LandingPage.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminView from '../views/AdminDashboard.vue'
import StaffView from '../views/StaffDashboard.vue'
import UserView from '../views/UserDashboard.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminView }, 
  { path: '/staff', component: StaffView }, 
  { path: '/user', component: UserView },  
  { path: '/:pathMatch(.*)*', redirect: '/' } 
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router