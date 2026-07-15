<template>
  <div class="p-4">
    <h3>Search User or Staff</h3>
    
    <input v-model="searchId" class="form-control" placeholder="Enter ID (e.g., TS001)" />
    <button @click="searchData" class="btn btn-primary mt-2">Search</button>
    
    <div v-if="result" class="mt-4">
      <p>User Id: {{ result.userid }}</p>
      <p>Name: {{ result.name }}</p>
      <p>Email: {{ result.email }}</p>
      <p>Role: {{ result.role }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const searchId = ref('');
const result = ref(null);

const searchData = async () => {
  try {

    const res = await axios.get(
      `http://127.0.0.1:5000/api/admin/search-user?query=${searchId.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      }
    );

    result.value = {
      userid: searchId.value,
      name: res.data.data.name,
      email: res.data.data.email,
      role: "User/Staff"
    };

  } catch (error) {
    alert("User not found");
    result.value = null;
  }
};
</script>