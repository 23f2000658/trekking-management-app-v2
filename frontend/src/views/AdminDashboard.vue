<template>
  <div class="d-flex" id="wrapper">
    <div class="bg-dark border-right text-white" id="sidebar-wrapper" style="width: 250px; min-height: 100vh;">
      <div class="sidebar-heading p-4 font-weight-bold">Trekking Admin</div>
      <div class="list-group list-group-flush">
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'dashboard'">Dashboard</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'treks'">Manage Treks</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'staff'">Manage Staff</button>
        <button class="list-group-item bg-dark text-white" @click="activeTab = 'users'">Manage Users</button>
      </div>
    </div>

    <main class="content flex-grow-1 p-4">
      <component :is="activeComponent" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import DashboardHome from './DashboardHome.vue'; 
import ManageTreks from './ManageTreks.vue';
import ManageStaff from './ManageStaff.vue';
import ManageUsers from './ManageUsers.vue';

const activeTab = ref('dashboard');

const activeComponent = computed(() => {
  const components = {
    dashboard: DashboardHome,
    treks: ManageTreks,
    staff: ManageStaff,
    users: ManageUsers
  };
  return components[activeTab.value];
});
</script>

<style scoped>
#sidebar-wrapper { transition: all 0.3s; }
.list-group-item { border: none; padding: 15px 20px; }
.list-group-item:hover { background-color: #495057 !important; }
</style>

