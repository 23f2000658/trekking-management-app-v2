<template>
  <div class="container mt-5">
    <h3>Create New Trek</h3>
    <button class="btn btn-info" @click="goToAllTreks">All Treks</button>
    <form @submit.prevent="handletreks" class="card p-4">
      <input v-model="form.trek_id" placeholder="Trek Id" class="form-control mb-2" required>
      <input v-model="form.name" placeholder="Trek Name" class="form-control mb-2" required>
      <input v-model="form.location" placeholder="Location" class="form-control mb-2" required>
      <select v-model="form.difficulty" class="form-control mb-2">
        <option>Easy</option><option>Medium</option><option>Hard</option>
      </select>
      <input type="number" v-model="form.duration" placeholder="Duration (Days)" class="form-control mb-2">
      <input type="number" v-model="form.total_slots" placeholder="Total Slots" class="form-control mb-2">
      <label>Start Date</label>
      <input type="date" v-model="form.start_date" class="form-control mb-2">
      <label>End Date</label>
      <input type="date" v-model="form.end_date" class="form-control mb-2">
      <input v-model="form.staff_id" placeholder="Staff id " class="form-control mb-2" required>
      
      <button type="submit" class="btn btn-success">Create Trek</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = reactive({
  trek_id: '',
  name: '',
  location: '',
  difficulty: 'Easy',
  duration: '', 
  total_slots: '',
  start_date: '',
  end_date: '',
  staff_id: ''
});


const handletreks = async () => {
  try {
    await axios.post('http://127.0.0.1:5000/api/admin/create-trek', {
      trek_id: form.trek_id,
      name: form.name,
      location: form.location,
      difficulty: form.difficulty,
      duration: form.duration,
      total_slots: form.total_slots,
      start_date: form.start_date,
      end_date: form.end_date,
      staff_id: form.staff_id
    });

    alert("Trek Registered Successfully!");
  } catch (error) {
    console.error("Trek Registration failed:", error.response ? error.response.data : error.message);
    alert("Error: Could not register trek.");
  }
};

const goToAllTreks = () => {
  router.push('/manage-treks');
};
</script>