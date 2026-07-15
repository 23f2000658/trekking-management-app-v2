<template>
  <div class="d-flex" id="wrapper">
    <div class="bg-success text-white" id="sidebar-wrapper" style="width: 250px; min-height: 100vh;">
      <div class="sidebar-heading p-4 font-weight-bold">Trekker Portal</div>
      <div class="list-group list-group-flush">
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'dashboard'">Dashboard</a>
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'browse'">Browse Treks</a>
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'Booked'">Booked Treks</a>
        <a href="#" class="list-group-item list-group-item-action bg-success text-white" @click="activeTab = 'history'">History</a>
      </div>
    </div>

    <div id="page-content-wrapper" class="w-100">
      <nav class="navbar navbar-light bg-light border-bottom p-3">
        <span class="navbar-brand">Welcome, User</span>
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
      </nav>

      <div class="container-fluid p-4">
        <div v-if="activeTab === 'dashboard'">
          <h4>Available Treks</h4>
          <div class="row">

                <div
                    class="col-md-4 mb-3"
                    v-for="trek in treks"
                    :key="trek.id"
                >

                    <div class="card shadow">

                        <div class="card-body">

                            <h5>{{ trek.name }}</h5>

                            <p>

                                {{ trek.location }}

                                <br>

                                {{ trek.difficulty }}

                                <br>

                                {{ trek.duration }} Days

                                <br>

                                Slots : {{ trek.available_slots }}

                            </p>

                            <button
    class="btn"
    :class="trek.already_booked ? 'btn-secondary' : 'btn-success'"
    :disabled="trek.already_booked"
    @click="bookTrek(trek.id)"
>
    {{ trek.already_booked ? "Already Booked" : "Book Now" }}
</button>

                        </div>

                    </div>

                </div>

            </div>
        </div>

        
        <div v-if="activeTab === 'browse'">

                <h4>Explore All Treks</h4>

                <input
                    type="text"
                    class="form-control mb-3"
                    placeholder="Search treks..."
                    v-model="search"
                >

                <div class="row">

                    <div
                        class="col-md-4 mb-3"
                        v-for="trek in filteredTreks"
                        :key="trek.id"
                    >

                        <div class="card shadow">

                            <div class="card-body">

                                <h5>{{ trek.name }}</h5>

                                <p>

                                    {{ trek.location }}<br>

                                    {{ trek.difficulty }}<br>

                                    {{ trek.duration }} Days<br>

                                    Slots : {{ trek.available_slots }}

                                </p>

                                <button
    class="btn"
    :class="trek.already_booked ? 'btn-secondary' : 'btn-success'"
    :disabled="trek.already_booked"
    @click="bookTrek(trek.id)"
>
    {{ trek.already_booked ? "Already Booked" : "Book Now" }}
</button>

                            </div>

                        </div>

                    </div>

                </div>
        </div>

        <div v-if="activeTab === 'Booked'">

    <h4>My Booked Treks</h4>

    <table class="table table-bordered mt-3">

        <thead>
            <tr>
                <th>Trek</th>
                <th>Location</th>
                <th>Duration</th>
                <th>Booking Date</th>
                <th>Status</th>
            </tr>
        </thead>

        <tbody>

            <tr
                v-for="booking in bookings"
                :key="booking.booking_id"
            >

                <td>{{ booking.trek_name }}</td>
                <td>{{ booking.location }}</td>
                <td>{{ booking.duration }} Days</td>
                <td>{{ booking.booking_date }}</td>
                <td>

                    <span class="badge bg-primary">

                        {{ booking.status }}

                    </span>

                </td>

            </tr>

        </tbody>

    </table>

</div>

        <div v-if="activeTab === 'history'">

    <div class="d-flex justify-content-between align-items-center mb-3">

        <h4>Trekking History</h4>

        <button
            class="btn btn-success"
            @click="exportCSV"
        >
            Export CSV
        </button>

    </div>

    <table class="table mt-3">
            <thead><tr><th>Trek Name</th><th>Date</th><th>Status</th></tr></thead>
            <tbody>
              <tr
    v-for="item in history"
    :key="item.trek_name + item.booking_date"
>

    <td>{{ item.trek_name }}</td>

    <td>{{ item.booking_date }}</td>

    <td>

        <span class="badge bg-success">

            {{ item.status }}

        </span>

    </td>

</tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import api from "../axios";

import { ref, onMounted, computed } from "vue";

const search = ref("");

const filteredTreks = computed(() => {
    return treks.value.filter(t =>
        t.name.toLowerCase().includes(search.value.toLowerCase()) ||
        t.location.toLowerCase().includes(search.value.toLowerCase()) ||
        t.difficulty.toLowerCase().includes(search.value.toLowerCase())
    );
});

const treks = ref([]);
const bookings = ref([]);
const history = ref([]);

const bookTrek = async (trekId) => {
  try {
    const res = await api.post("/api/user/book", {
      trek_id: trekId,
    });

    alert(res.data.message);

    await fetchTreks(); 
    await fetchBookings();
    await fetchHistory();

  } catch (err) {
    alert(err.response.data.error);
  }
};

const fetchTreks = async () => {

    try{

        const res = await api.get("/api/user/treks");
        console.log(res.data);
        treks.value = res.data;

    }

    catch(err){

        console.log(err);

    }

};

const fetchBookings = async () => {

    try{

        const res = await api.get("/api/user/bookings");
        bookings.value = res.data;

    }

    catch(err){

        console.log(err);

    }

};

const fetchHistory = async () => {

    try{

        const res = await api.get("/api/user/history");
        history.value = res.data;

    }

    catch(err){

        console.log(err);

    }

};

onMounted(() => {

    fetchTreks();
    fetchBookings();
    fetchHistory();

});

const activeTab = ref('dashboard');

const exportCSV = async () => {

    try {

        const res = await api.get(
            "/api/user/export-csv",
            {
                responseType: "blob"
            }
        );

        const url = window.URL.createObjectURL(
            new Blob([res.data])
        );

        const link = document.createElement("a");

        link.href = url;

        link.download = "trek_history.csv";

        document.body.appendChild(link);

        link.click();

        link.remove();

    }

    catch(err){

        console.log(err);

        alert("Export Failed");

    }

};

const logout = () => {
  localStorage.clear();
  window.location.href = '/login';
};
</script>

<style scoped>
#sidebar-wrapper { transition: all 0.3s; }
.list-group-item { border: none; padding: 15px 20px; background: transparent; }
.list-group-item:hover { background: rgba(255,255,255,0.1) !important; }
</style>
