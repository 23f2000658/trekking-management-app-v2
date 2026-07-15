<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between mb-3">
      <h3>Manage Trekkers (Users)</h3>
      <input type="text" v-model="searchQuery" placeholder="Search users..." class="form-control w-25">
    </div>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filteredUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.is_active ? 'Active' : 'Inactive' }}</td>
          <td>
            <button class="btn btn-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../axios.js';

const users = ref([]);
const searchQuery = ref('');


const fetchUsers = async () => {
  try {
    const res = await api.get('/api/users');
    users.value = res.data;
  } catch (err) {
    console.error("Error fetching users:", err);
  }
};


const filteredUsers = computed(() => {
  return users.value.filter(u => 
    u.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});


const deleteUser = async (id) => {
  if (confirm("Are you sure you want to delete this user?")) {
    try {
      await api.delete(`/api/admin/user/${id}`);
      alert("User deleted!");
      fetchUsers();
    } catch (err) {
      alert("Error deleting user!");
    }
  }
};

onMounted(fetchUsers);
</script>