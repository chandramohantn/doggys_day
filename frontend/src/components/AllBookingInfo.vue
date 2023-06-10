<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ username }}</h1>
        </div>

        <div class="content-container">
            <h2>All Bookings Info:</h2>
            <!-- <p> {{ receivedData }} </p> -->
            <div class="inner-container">
                <div class="small-container caretaker-item" v-for="item in receivedData" :key="item.id"
                    @click="handleClick(item.id)">
                    <p>{{ item.id }},</p>
                    <p>{{ item.owner_id }},</p>
                    <p>{{ item.caretaker_id }}, </p>
                    <p>{{ item.instruction }}, </p>
                    <p>{{ item.date_of_booking }}</p>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import './styles.css';
import axios from 'axios';

axios.interceptors.request.use(config => {
    const access_token = localStorage.getItem('access_token');
    const token_type = localStorage.getItem('token_type');

    if (access_token && token_type) {
        config.headers['Authorization'] = `${token_type} ${access_token}`;
    }

    return config;
});

export default {
    name: 'AllBookingInfo',
    data() {
        return {
            username: '',
            receivedData: '',
        }
    },
    created() {
        this.username = localStorage.getItem('username');
        this.receivedData = JSON.parse(this.$route.params.responseData)
    },
    methods: {
        async handleClick(booking_id) {
            const formData = {
                booking_id: booking_id,
            };

            try {
                axios.get(`http://127.0.0.1:8000/api/v1/owner/booking/${booking_id}`, { params: formData })
                    .then(response => {
                        console.warn('Booking Info:', response.data);
                        this.responseData = response.data;
                        console.warn(typeof this.responseData);
                        console.warn(this.responseData);
                        this.$router.push({ name: 'BookingInfo', params: { responseData: JSON.stringify(response.data) } })
                    })
                    .catch(error => {
                        console.warn('Fetching Bookings Failed:', error.response.data);
                    });
            } catch (error) {
                console.error('Fetching Bookings Failed:', error.response.data);
            }
        },
    },
};
</script>