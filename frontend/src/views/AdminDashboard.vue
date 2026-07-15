<template>
  <div class="d-flex" id="wrapper">
    <div class="bg-dark border-right text-white" id="sidebar-wrapper" style="width: 250px; min-height: 100vh;">
      <div class="sidebar-heading p-4 font-weight-bold">Trekking Admin</div>
      <div class="list-group list-group-flush">
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'dashboard'">Dashboard</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'treks'">Manage Treks</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'staff'">Manage Staff</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'users'">Manage Users</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'search'">Search User/Staff</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'Booking'">Booking Records</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'Reports'">History and Reports</button>
      </div>
    </div>

    <div id="page-content-wrapper" class="w-100">
      <nav class="navbar navbar-light bg-light border-bottom p-3">
        <span class="navbar-brand">Admin Dashboard</span>
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
      </nav>

    <main class="content flex-grow-1 p-4">
      <component :is="activeComponent" />
    </main>
  </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DashboardHome from './DashboardHome.vue'; 
import ManageTreks from './ManageTreks.vue';
import ManageStaff from './ManageStaff.vue';
import ManageUsers from './ManageUsers.vue';
import SearchPage from './SearchPage.vue';
import BookingRecords from './Bookings.vue';
import History$Reports from './TrekReports.vue';

const activeTab = ref('dashboard');



const logout = () => {
  localStorage.clear();
  window.location.href = '/login';
};

const activeComponent = computed(() => {
  const components = {
    dashboard: DashboardHome,
    treks: ManageTreks,
    staff: ManageStaff,
    users: ManageUsers,
    search: SearchPage,
    Booking: BookingRecords,
    Reports: History$Reports
  };
  return components[activeTab.value];
});
</script>

<style scoped>
#sidebar-wrapper { transition: all 0.3s; }
.list-group-item { border: none; padding: 15px 20px; }
.list-group-item:hover { background-color: #495057 !important; }
</style>

