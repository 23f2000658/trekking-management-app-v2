
<template>
  <div class="p-3">
    <h5>All Booking Records</h5>
    
    
    <p v-if="loading">Data load ho raha hai...</p>
    
    
    <p v-else-if="bookings.length === 0">Koi booking record nahi mila!</p>
    
    
    <table v-else class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>Booking ID</th>
          <th>User ID</th>
          <th>Username</th>
          <th>Trek</th>
          <th>Location</th>
          <th>Booking Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="booking in bookings" :key="booking.id">

          <td>{{ booking.id }}</td>

          <td>{{ booking.user_id }}</td>

          <td>{{ booking.user_name }}</td>

          <td>{{ booking.trek_name }}</td>

          <td>{{ booking.location }}</td>

          <td>{{ booking.date }}</td>

          <td>
            <span
              class="badge"
              :class="booking.status === 'Booked'
                ? 'bg-primary'
                : booking.status === 'Completed'
                ? 'bg-success'
                : 'bg-danger'"
            >
              {{ booking.status }}
            </span>
          </td>

        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../axios';

const bookings = ref([]);
const loading = ref(true); 

onMounted(async () => {
  console.log("Bookings component loaded");
  try {
    const res = await axios.get('/api/bookings');
    bookings.value = res.data;
  } catch (err) {
    console.error("API Error:", err);
  } finally {
    loading.value = false; 
  }
});
</script>