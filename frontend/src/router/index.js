import { createRouter, createWebHistory } from 'vue-router'

import LandingPage from '../views/LandingPage.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminView from '../views/AdminDashboard.vue'
import StaffView from '../views/StaffDashboard.vue'
import UserView from '../views/UserDashboard.vue'
import ManageTreks from '../views/AllTreks.vue'
import ManageStaff from '../views/ManageStaff.vue'
import AllTreks from '../views/ManageTreks.vue'
import AllStaff from '../views/AllStaff.vue'
import Allusers from '../views/ManageUsers.vue'
import ManageTrek from '../views/ManageTrek.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminView, meta: { requiresAuth: true, role: 'admin' } }, 
  { path: '/staff', component: StaffView, meta: { requiresAuth: true, role: 'staff' } }, 
  { path: '/user', component: UserView, meta: { requiresAuth: true, role: 'user' } },  
  { path: '/manage-treks', component: ManageTreks, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/manage-staff', component: ManageStaff, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/all-treks', component: AllTreks, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/all-staff', component: AllStaff, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/all-users', component: Allusers, meta: { requiresAuth: true, role: 'admin' } },
  {
  path: '/staff/manage-trek/:id',
  component: ManageTrek,
  meta: { requiresAuth: true, role: 'staff' }
  },
  { path: '/:pathMatch(.*)*', redirect: '/' } 
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('role'); 

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login'); 
    } else if (to.meta.role && to.meta.role !== userRole) {
      next('/'); 
    } else {
      next(); 
    }
  } else {
    next();
  }
});

export default router