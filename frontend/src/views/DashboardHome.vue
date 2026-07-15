<template>
  <div class="p-4">
    <h3>Dashboard</h3>
    <div class="row">
      
      <div class="col-md-3" v-for="(value, key) in stats" :key="key">
        <div class="card p-3 shadow-sm">
          <h6>{{ formatLabel(key) }}</h6>
          <h3>{{ value }}</h3>
        </div>
      </div>
    </div>
    <hr>
    <h5>Recent Bookings</h5>
    <table class="table table-bordered mt-3" v-if="recentBookings.length">
  <thead>
    <tr>
      <th>User</th>
      <th>Trek</th>
      <th>Date</th>
      <th>Status</th>
    </tr>
  </thead>

  <tbody>
    <tr v-for="booking in recentBookings" :key="booking.id">
      <td>{{ booking.user_name }}</td>
      <td>{{ booking.trek_name }}</td>
      <td>{{ booking.date }}</td>
      <td>{{ booking.status }}</td>
    </tr>
  </tbody>
</table>

<p v-else>No recent bookings.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from '../axios'; 
import { useRouter } from 'vue-router';

const recentBookings = ref([]);
const router = useRouter();
const stats = ref({ total_treks: 0, total_users: 0, total_staff: 0, total_bookings: 0 });

const formatLabel = (key) => {
  if (typeof key !== 'string') return key;
  return key.replace('_', ' ').toUpperCase();
};
onMounted(async () => {
  console.log("Token:", localStorage.getItem("token"));
  console.log("Axios:", axios.defaults.baseURL);
  try {
    const response = await axios.get('/api/admin/stats');
    stats.value = response.data;

    const bookingRes = await axios.get('/api/bookings');
    recentBookings.value = bookingRes.data
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 5);

  } catch (error) {

    console.log("Status:", error.response?.status);
    console.log("Response:", error.response?.data);

    console.error(error);
  }
});
</script>