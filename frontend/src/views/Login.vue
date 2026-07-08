<template>
  <div class="login-wrapper d-flex align-items-center justify-content-center">
    <div class="card p-4 shadow-sm" style="width: 100%; max-width: 400px;">
      <h3 class="text-center mb-4">Login</h3>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" v-model="form.username" class="form-control" required>
        </div>
        
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="form.password" class="form-control" required>
        </div>
        
        <button type="submit" class="btn btn-primary w-100">Log in</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = reactive({
  username: '',
  password: ''
});

const handleLogin = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/auth/login', form);
    
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('role', response.data.role);
    
    alert("Login Successful!");

    if (response.data.role === 'admin') router.push('/admin');
    else if (response.data.role === 'staff') router.push('/staff');
    else router.push('/user');

  } catch (error) {
    alert("Invalid Credentials or Server Error!");
  }
};
</script>

<style scoped>

.login-wrapper {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  border: none;
  border-radius: 12px;
}

.btn-primary {
  padding: 10px;
  font-weight: 600;
}
</style>


