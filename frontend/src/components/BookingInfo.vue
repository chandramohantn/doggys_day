<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ username }}</h1>
        </div>

        <div class="content-container">
            <h2>Booking Info:</h2>
            <ul>
                <p> {{ receivedData }} </p>
            </ul>
            <button @click="handleAllBookings">View All Bookings</button>
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
    name: 'BookingInfo',
    data() {
        return {
            username: '',
            receivedData: ''
        }
    },
    created() {
        this.username = localStorage.getItem('username');
        this.userid = localStorage.getItem('userid');
        this.receivedData = JSON.parse(this.$route.params.responseData)
    },
    methods: {
        async handleAllBookings() {
            const formData = {
                owner_id: this.userid
            };

            try {
                axios.get(`http://127.0.0.1:8000/api/v1/owner/booking/${this.userid}`, { params: formData })
                    .then(response => {
                        console.warn('All Booking Info:', response.data);
                        this.responseData = response.data;
                        console.warn(typeof this.responseData);
                        console.warn(this.responseData);
                        this.$router.push({ name: 'AllBookingInfo', params: { responseData: JSON.stringify(response.data) } })
                    })
                    .catch(error => {
                        console.warn('Fetching Booking Info Failed:', error.response.data);
                    });
            } catch (error) {
                console.error('Fetching Booking Info Failed:', error.response.data);
            }
        },
    },
};
</script>