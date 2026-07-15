<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between mb-3">
      <h3>Manage Treks</h3>
      
        <button class="btn btn-secondary" @click="goBack">
        Back to Manage Treks
        </button>
    </div>

    
    <div v-if="showForm" class="card p-3 mb-4">
      
    </div>

    
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>Location</th>
          <th>Difficulty</th>
          <th>Slots</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trek in treks" :key="trek.id">
          <td>{{ trek.name }}</td>
          <td>{{ trek.location }}</td>
          <td>{{ trek.difficulty }}</td>
          <td>{{ trek.available_slots }} / {{ trek.total_slots }}</td>
          <td>
            <button class="btn btn-danger btn-sm" @click="deleteTrek(trek.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../axios.js';

const treks = ref([]);
const showForm = ref(false);

const fetchTreks = async () => {
  const res = await api.get('/api/treks');
  treks.value = res.data;
};

const deleteTrek = async (id) => {
  if (confirm("Are you sure?")) {
    try {
      await api.delete(`/api/admin/trek/${id}`);
      alert("Trek deleted!");
      fetchTreks(); 
    } catch (err) {
      alert("Some error happened");
    }
  }
};

onMounted(fetchTreks);


import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  
  router.push('/all-treks');
};


</script>