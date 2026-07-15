<template>
  <div class="container-fluid p-4">
    <h3 class="mb-4">Create New Trekking Staff</h3>
    <button class="btn btn-info" @click="goTostaff">All Staff</button>

    <form @submit.prevent="createStaff" class="bg-white p-4 shadow-sm rounded">
      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label">Staff id</label>
          <input type="text" v-model="staff.staff_id" placeholder="staff_<staffname>" class="form-control" required>
        </div>
        <div class="col-md-6">
          <label class="form-label">Full Name</label>
          <input type="text" v-model="staff.name" class="form-control" required>
        </div>
        <div class="col-md-6">
          <label class="form-label">Email Address</label>
          <input type="email" v-model="staff.email" class="form-control" required>
        </div>
      </div>

      <div class="row mb-3">
        
        <div class="col-md-6">
          <label class="form-label">Password</label>
          <input type="password" v-model="staff.password" class="form-control" required>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Confirm Password</label>
        <input type="password" v-model="staff.confirmPassword" class="form-control" required>
      </div>

      <div class="mb-3">
        <label class="form-label">Status</label>
        <select v-model="staff.status" class="form-select">
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>
      </div>

      <div class="d-flex gap-2">
        <button type="button" class="btn btn-outline-secondary px-4">Cancel</button>
        <button type="submit" class="btn btn-primary px-4">Create Staff</button>
      </div>
    </form>

    <div class="alert alert-info mt-3 d-flex align-items-center">
      <i class="bi bi-info-circle me-2"></i>
      The staff will receive an email with login credentials.
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; 

const router = useRouter();

const staff = reactive({
  staff_id: '',
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  status: 'Active'
});

const createStaff = async () => { 
  if (staff.password !== staff.confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  try {
      await axios.post('http://127.0.0.1:5000/api/admin/create-staff', {
      user_id: staff.staff_id, 
      username: staff.name,
      email: staff.email,
      password: staff.password,
      status: staff.status
    });
  
    alert("Registration Successful!");
  }
    catch (error) {
    console.error("Registration failed:", error.response ? error.response.data : error.message);
    alert("Error: Could not register user.");
  }
};

const goTostaff = () => {
  router.push('/all-staff');
};
</script>