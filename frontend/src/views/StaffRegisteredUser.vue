<template>

<div class="container mt-4">

    <h3 class="mb-3">Registered Users</h3>

    <div class="card shadow">

        <div class="card-body">

            <table class="table table-bordered table-hover">

                <thead class="table-dark">

                    <tr>

                        <th>Trek</th>
                        <th>User ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Booking Date</th>
                        <th>Status</th>
                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr
                        v-for="user in participants"
                        :key="user.booking_id"
                    >

                        <td>{{ user.trek_name }}</td>
                        <td>{{ user.user_id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.booking_date }}</td>

                        <td>

                            <select
                                class="form-select"
                                v-model="user.status"
                            >

                                <option>Booked</option>
                                <option>Completed</option>

                            </select>

                        </td>

                        <td>

                            <button
                                class="btn btn-success btn-sm"
                                @click="updateBooking(user)"
                            >

                                Save

                            </button>

                        </td>

                    </tr>

                    <tr v-if="participants.length==0">

                        <td colspan="7" class="text-center">

                            No Registered Users

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

</div>

</template>

<script setup>

import { ref, onMounted } from "vue";
import api from "../axios";

const participants = ref([]);

const fetchParticipants = async () => {

    try{

        const res = await api.get("/api/staff/participants");

        participants.value = res.data;

    }

    catch(err){

        console.log(err);

    }

}

const updateBooking = async (user) => {

    try{

        await api.put(

            `/api/staff/booking/${user.booking_id}`,

            {

                status: user.status

            }

        );

        alert("Booking Updated Successfully");

    }

    catch(err){

        console.log(err);

        alert("Update Failed");

    }

}

onMounted(() => {

    fetchParticipants();

});

</script>