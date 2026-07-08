<template>
  <div class="d-flex" id="wrapper">
    <div class="bg-primary text-white" id="sidebar-wrapper" style="width: 250px; min-height: 100vh;">
      <div class="sidebar-heading p-4 font-weight-bold">Staff Portal</div>
      <div class="list-group list-group-flush">
        <a href="#" class="list-group-item list-group-item-action bg-primary text-white" @click="activeTab = 'dashboard'">My Dashboard</a>
        <a href="#" class="list-group-item list-group-item-action bg-primary text-white" @click="activeTab = 'my-treks'">My Assigned Treks</a>
        <a href="#" class="list-group-item list-group-item-action bg-primary text-white" @click="activeTab = 'profile'">Profile</a>
      </div>
    </div>

    <div id="page-content-wrapper" class="w-100">
      <nav class="navbar navbar-light bg-light border-bottom p-3">
        <span class="navbar-brand">Staff Dashboard</span>
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
      </nav>

      <div class="container-fluid p-4">
        <div v-if="activeTab === 'dashboard'">
          <h4>Welcome, Staff Member</h4>
          <div class="row mt-3">
            <div class="col-md-4"><div class="card p-3 shadow-sm bg-light"><h6>Assigned Treks</h6><h3>3</h3></div></div>
            <div class="col-md-4"><div class="card p-3 shadow-sm bg-light"><h6>Total Participants</h6><h3>32</h3></div></div>
          </div>
        </div>

        <div v-if="activeTab === 'my-treks'">
          <h4>Assigned Treks</h4>
          <table class="table mt-3 border">
            <thead class="table-dark">
              <tr><th>Trek Name</th><th>Dates</th><th>Participants</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>Everest Base Camp</td>
                <td>31 May 2026</td>
                <td>12</td>
                <td><button class="btn btn-sm btn-info">Manage</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const activeTab = ref('dashboard');

const logout = () => {
  localStorage.clear();
  window.location.href = '/login';
};
</script>

<style scoped>
#sidebar-wrapper { transition: all 0.3s; }
.list-group-item { border: none; padding: 15px 20px; background: transparent; }
.list-group-item:hover { background: rgba(255,255,255,0.1) !important; }
</style>
