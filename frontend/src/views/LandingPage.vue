<template>
  <div class="landing-wrapper">
    <div class="container d-flex flex-column justify-content-center align-items-center h-100 text-white">
      <h1 class="display-3 fw-bold">Trekking Management App</h1>
      <p class="lead mb-4">Adventure is calling. Manage your treks with ease.</p>
      
      <div class="d-flex gap-3">
        <router-link to="/login" class="btn btn-primary btn-lg px-4">Login</router-link>
        <router-link to="/register" class="btn btn-outline-light btn-lg px-4">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script>

import bgImage from '@/assets/mad_02_image.jpg'

export default {
  name: 'LandingPage',
  data() {
    return {
      bgImage
    }
  }
}
</script>

<style scoped>
.landing-wrapper {

  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url('@/assets/mad_02_image.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  width: 100%;
}

.btn:hover {
  transform: scale(1.05);
  transition: 0.3s;
}
</style>

