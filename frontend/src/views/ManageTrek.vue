<template>

<div class="container mt-4">

<h2>Manage Trek</h2>

<h4>{{ trek?.name }}</h4>

<div class="card p-3 mt-3">

<label>Available Slots</label>

<input
type="number"
class="form-control"
v-model="trek.available_slots"
/>



</div>

<div class="card p-3 mt-3">

<label>Status</label>
<th>Action</th>

<select
v-model="trek.status"
class="form-control"
>

<option>Pending</option>
<option>Approved</option>
<option>Open</option>
<option>Closed</option>
<option>Completed</option>

</select>

</div>

<div class="mt-3">

    <button
        class="btn btn-success"
        @click="saveChanges"
    >
        Save Changes
    </button>

</div>

<div class="card mt-4">

    <div class="card-header">

        <h5>Registered Users</h5>

    </div>

    <div class="card-body">

        <table class="table table-bordered">

            <thead class="table-dark">

                <tr>

                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Booking Date</th>
                    <th>Status</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="user in participants"
                    :key="user.id"
                >

                    <td>{{ user.user_id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.booking_date }}</td>
                    <td>

<select
    v-model="user.status"
    class="form-control"
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

                <tr v-if="participants.length == 0">

                    <td colspan="5" class="text-center">

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
import { useRoute } from "vue-router";
import api from "../axios";

const trek = ref({});

const route = useRoute();

const participants = ref([]);

const updateBooking = async (user) => {

    try{

        await api.put(

            `/api/staff/booking/${user.booking_id}`,

            {

                status: user.status

            }

        );

        alert("Booking Updated");

    }

    catch(err){

        console.log(err);

        alert("Update Failed");

    }

};

const fetchParticipants = async () => {

    try {

        const res = await api.get(
            `/api/staff/trek/${route.params.id}/participants`
        );

        participants.value = res.data;

    } catch (err) {

        console.log(err);

    }

};

const fetchTrek = async () => {

    try{

        const res = await api.get(
            `/api/staff/trek/${route.params.id}`
        );

        trek.value = res.data;

    }

    catch(err){

        console.log(err);

    }

}

onMounted(() => {

    fetchTrek();
    fetchParticipants();

});

const saveChanges = async () => {

    try{

        await api.put(

            `/api/staff/trek/${route.params.id}`,

            {

                available_slots: trek.value.available_slots,

                status: trek.value.status

            }

        );

        alert("Trek Updated Successfully!");

    }

    catch(err){

        console.log(err);

        alert("Update Failed");

    }

}
</script>