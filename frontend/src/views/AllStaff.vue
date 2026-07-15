<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between mb-3">
      <h3>All Staff</h3>
      
        <button class="btn btn-secondary" @click="goBack">
        Back to Manage Staff
        </button>
    </div>

    
    <div v-if="showForm" class="card p-3 mb-4">
      
    </div>

    
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Isactive</th>
          <th>Created at</th>

        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.is_active }}</td>
          <td>{{ user.created_at }}</td>
          <td>

<div v-if="!user.assigned">

<select
v-model="user.selectedTrekId"
class="form-control form-control-sm"
>

<option value="">Select Trek</option>

<option
v-for="trek in allTreks"
:key="trek.id"
:value="trek.id"
>

{{ trek.name }}

</option>

</select>

</div>

<div v-else>

<span class="badge bg-success">
{{ user.trek_name }}
</span>

</div>

</td>

<td>

<button
v-if="!user.assigned"
class="btn btn-primary btn-sm"
@click="assignTrek(user)"
>

Assign

</button>

<span
v-else
class="text-success fw-bold"
>

✔ Assigned

</span>

</td>
          <td>
            <button class="btn btn-danger btn-sm" @click="deleteTrek(user.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../axios.js';

const users = ref([]);
const allTreks = ref([]);
const showForm = ref(false);

const fetchstaff = async () => {
  const staffRes = await api.get('/api/staff');
  console.log(staffRes.data);
  console.log(typeof staffRes.data);
  console.log("Asli Data:", staffRes.data[0]);
  const trekRes = await api.get('/api/treks');
  users.value = staffRes.data.map(u => ({ ...u, selectedTrekId: '' }));
  allTreks.value = trekRes.data;
};


const assignTrek = async (user) => {
  console.log("Assigning:", { staff: user.user_id, trek: user.selectedTrekId });
  if (!user.selectedTrekId) {
    alert("Please select a trek first!");
    return;
  }
  
  try {
    await api.post('/api/admin/assign-trek', {
      staff_id: user.user_id,
      trek_id: user.selectedTrekId
    });
    fetchstaff(); 
    alert(`Successfully assigned`);
  } catch (err) {
    alert("Error assigning trek");
  }
};

const deleteTrek = async (id) => {
  if (confirm("Are you sure?")) {
    try {
      await api.delete(`/api/admin/staff/${id}`);
      alert("staff deleted!");
      fetchstaff(); 
    } catch (err) {
      alert("Some error happened");
    }
  }
};

onMounted(fetchstaff);


import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  
  router.push('/manage-staff');
};


</script>