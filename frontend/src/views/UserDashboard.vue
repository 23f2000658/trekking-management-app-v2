<template>
  <div class="d-flex" id="wrapper">
    <div class="bg-success text-white" id="sidebar-wrapper" style="width: 250px; min-height: 100vh;">
      <div class="sidebar-heading p-4 font-weight-bold">Trekker Portal</div>
      <div class="list-group list-group-flush">
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'dashboard'">Dashboard</a>
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'browse'">Browse Treks</a>
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'history'">History</a>
      </div>
    </div>

    <div id="page-content-wrapper" class="w-100">
      <nav class="navbar navbar-light bg-light border-bottom p-3">
        <span class="navbar-brand">Welcome, User</span>
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
      </nav>

      <div class="container-fluid p-4">
        <div v-if="activeTab === 'dashboard'">
          <h4>Available Treks</h4>
          <div class="row mt-3">
            <div class="col-md-4">
              <div class="card shadow-sm">
                <div class="card-body">
                  <h5 class="card-title">Everest Base Camp</h5>
                  <p class="card-text">Nepal | 12 Days | Slots: 8</p>
                  <button class="btn btn-success w-100">Book Now</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'browse'">
          <h4>Explore All Treks</h4>
          <input type="text" class="form-control mb-3" placeholder="Search treks...">
          </div>

        <div v-if="activeTab === 'history'">
          <h4>Trekking History</h4>
          <table class="table mt-3">
            <thead><tr><th>Trek Name</th><th>Date</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td>Roopkund Trek</td><td>10 Apr 2026</td><td><span class="badge bg-success">Completed</span></td></tr>
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
