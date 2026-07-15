<template>
  <div class="p-3">
    <h5>Trekking History & Reports</h5>
    
    
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card p-3 bg-light">
          <h6>Total Treks Conducted</h6>
          <h3>{{ stats.total_treks }}</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card p-3 bg-light">
          <h6>Most Popular Trek</h6>
          <p>{{ stats.top_trek }}</p>
        </div>
      </div>
    </div>

    
    <table class="table">
      <thead>
        <tr>
          <th>Trek Name</th>
          <th>Location</th>
          <th>Total Participants</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trek in trekHistory" :key="trek.id">
          <td>{{ trek.name }}</td>
          <td>{{ trek.location }}</td>
          <td>{{ trek.participant_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const trekHistory = ref([]);
const stats = ref({ total_treks: 0, top_trek: '' });

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:5000/api/trek-reports');
  trekHistory.value = res.data.history;
  stats.value = res.data.stats;
});
</script>