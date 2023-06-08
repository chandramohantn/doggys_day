<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ caretaker_name }}</h1>
        </div>

        <div class="content-container">
            <h2>Caretaker Info:</h2>
            <ul>
                <p> {{ receivedData }} </p>
            </ul>
            <button @click="handleBookCaretaker">Book</button>
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
    console.warn(config);
    return config;
});

export default {
    name: 'CaretakerInfo',
    data() {
        return {
            caretaker_name: '',
            receivedData: '',
            responseData: '',
        }
    },
    created() {
        this.userid = localStorage.getItem('userid');
        this.caretaker_name = this.$route.params.caretaker_name
        this.caretaker_id = this.$route.params.caretaker_id
        this.receivedData = JSON.parse(this.$route.params.responseData)
    },
    methods: {
        async handleBookCaretaker() {
            const formData = {
                owner_id: this.userid,
                caretaker_id: this.caretaker_id,
                instruction: 'NO instruction'
            };

            try {
                axios.post('http://127.0.0.1:8000/api/v1/owner/booking', formData)
                    .then(response => {
                        console.warn('Booking Info:', response.data);
                        this.responseData = response.data;
                        console.warn(typeof this.responseData);
                        console.warn(this.responseData);
                        this.$router.push({ name: 'BookingInfo', params: { responseData: JSON.stringify(response.data) } })
                    })
                    .catch(error => {
                        console.warn('Booking failed:', error.response.data);
                    });
            } catch (error) {
                console.error('Booking failed:', error.response.data);
            }
        },
    },
};
</script>