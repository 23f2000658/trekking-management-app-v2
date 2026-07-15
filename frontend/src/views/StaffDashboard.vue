<template>
  <div class="d-flex" id="wrapper">
    <div class="bg-primary text-white" id="sidebar-wrapper" style="width: 250px; min-height: 100vh;">
      <div class="sidebar-heading p-4 font-weight-bold">Staff Portal</div>
      <div class="list-group list-group-flush">
        <a href="#" class="list-group-item list-group-item-action bg-primary text-white" @click="activeTab = 'dashboard'">My Dashboard</a>
        <a href="#" class="list-group-item list-group-item-action bg-primary text-white" @click="activeTab = 'my-treks'">My Assigned Treks</a>
        <a href="#" class="list-group-item list-group-item-action bg-primary text-white" @click="activeTab = 'profile'">Registered Users</a>
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
            <div class="col-md-4">
              <div class="card p-3 shadow-sm bg-light">
                <h6>Assigned Treks</h6>
                <h3>{{ myTreks.length }}</h3>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card p-3 shadow-sm bg-light">
                <h6>Total Participants</h6>
                <h3>{{ totalParticipants }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'my-treks'">
          <h4>Assigned Treks</h4>
          <table class="table mt-3 border">
            <thead class="table-dark">
              <tr><th>Trek Name</th><th>Dates</th><th>Participants</th><th>Action</th></tr>
            </thead>
            <tbody>

              <tr v-for="trek in myTreks" :key="trek.id">

              <td>{{ trek.name }}</td>

              <td>{{ trek.start_date }} - {{ trek.end_date }}</td>

              <td>{{ trek.participants }}</td>

              <td>
                <button
                  class="btn btn-sm btn-primary"
                  @click="manageTrek(trek.id)"
                >
                  Manage
                </button>
              </td>

              </tr>

              <tr v-if="myTreks.length==0">
              <td colspan="4" class="text-center">
              No trek assigned yet.
              </td>
              </tr>

            </tbody>
          </table>
        </div>
        <div v-if="activeTab === 'profile'">
  <RegisteredUsers />
</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../axios";
import RegisteredUsers from "./StaffRegisteredUser.vue";

import { computed } from "vue";

import { useRouter } from "vue-router";

const router = useRouter();

const manageTrek = (id) => {
    router.push(`/staff/manage-trek/${id}`);
};

const totalParticipants = computed(() => {
  return myTreks.value.reduce((sum, trek) => sum + trek.participants, 0);
});

const activeTab = ref("dashboard");
const myTreks = ref([]);

const fetchMyTreks = async () => {
  try {
    const res = await api.get("/api/staff/my-treks");
    console.log("Treks:", res.data);
    myTreks.value = res.data;
  } catch (err) {
    console.log(err);
  }
};

onMounted(fetchMyTreks);

const logout = () => {
  localStorage.clear();
  window.location.href = "/login";
};
</script>

<style scoped>
#sidebar-wrapper { transition: all 0.3s; }
.list-group-item { border: none; padding: 15px 20px; background: transparent; }
.list-group-item:hover { background: rgba(255,255,255,0.1) !important; }
</style>
