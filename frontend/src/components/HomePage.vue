<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ username }}</h1>
        </div>

        <div class="content-container">
            <div class="inner-container">
                <div class="small-container card-container">
                    <p>Add Pet</p>
                    <button @click="handleAddPet">Add</button>
                </div>
                <div class="small-container card-container">
                    <p>Your Pets</p>
                    <button @click="handleShowPets">Show</button>
                </div>
                <div class="small-container card-container">
                    <p>Find Caretaker</p>
                    <button @click="handleFindCaretaker">Find</button>
                </div>
                <div class="small-container card-container">
                    <p>Your Bookings</p>
                    <button @click="handleShowBookings">Find</button>
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
    name: 'HomePage',
    data() {
        return {
            username: ''
        };
    },
    created() {
        this.username = localStorage.getItem('username');
        this.userid = localStorage.getItem('userid');
    },
    methods: {
        handleAddPet() {
            this.$router.push({ name: 'AddPet' });
        },
        handleShowPets() {
            const formData = {
                owner_id: this.userid
            };
            try {
                axios.get(`http://127.0.0.1:8000/api/v1/owner/owner_pet/${this.userid}`, { params: formData })
                    .then(response => {
                        console.log('Pet Info:', response.data);
                        this.$router.push({ name: 'PetInfo', params: { responseData: JSON.stringify(response.data) } })
                    })
                    .catch(error => {
                        console.warn('Fetching Pet Info Failed:', error.response.data);
                    });
            }
            catch (error) {
                console.warn('Fetching Pet Info Failed:', error.response.data);
            }
        },
        handleFindCaretaker() {
            const formData = {
                owner_id: this.userid
            };
            try {
                axios.get(`http://127.0.0.1:8000/api/v1/owner/recommend/${this.userid}`, { params: formData })
                    .then(response => {
                        console.log('Recommended Caretakers:', response.data);
                        this.$router.push({ name: 'FindCaretaker', params: { responseData: JSON.stringify(response.data) } })
                    })
                    .catch(error => {
                        console.warn('Recommending Careatkers failed:', error.response.data);
                    });
            }
            catch (error) {
                console.warn('Recommending Careatkers failed:', error.response.data);
            }
        },
        handleShowBookings() {
            const formData = {
                owner_id: this.userid
            };

            try {
                axios.get(`http://127.0.0.1:8000/api/v1/owner/owner_booking/${this.userid}`, { params: formData })
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

  