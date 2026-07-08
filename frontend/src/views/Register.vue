<template>
  <div class="register-wrapper d-flex align-items-center justify-content-center">
    <div class="card p-4 shadow-sm" style="width: 100%; max-width: 450px;">
      <h3 class="text-center mb-4">Create Account</h3>
      
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" v-model="form.name" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Email Address</label>
          <input type="email" v-model="form.email" class="form-control" required>
        </div>
        
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="form.password" class="form-control" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Confirm Password</label>
          <input type="password" v-model="form.confirmPassword" class="form-control" required>
        </div>
        
        <button type="submit" class="btn btn-success w-100 mt-2">Register</button>
      </form>
      
      <p class="text-center mt-3 text-muted small">
        Already have an account? <a href="/login" class="text-decoration-none">Login here</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  try {
    await axios.post('http://127.0.0.1:5000/api/auth/register', {
      username: form.name,
      email: form.email,
      password: form.password
    });

    alert("Registration Successful! Please login.");
    router.push('/login');
  } catch (error) {
    console.error("Registration failed:", error.response ? error.response.data : error.message);
    alert("Error: Could not register user.");
  }
};
</script>

<style scoped>
.register-wrapper {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  border: none;
  border-radius: 12px;
}
</style>

