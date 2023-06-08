<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ username }}</h1>
        </div>

        <div class="content-container">
            <form class="form-container">
                <h2 class="add_pet-title">Add Pet</h2>
                <div class="input-field">
                    <input type="text" placeholder="Petname" v-model="name" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Age" v-model="age" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Gender" v-model="gender" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Breed" v-model="breed" required />
                </div>
                <button class="signup-button" type="submit" @click="submitForm">Submit</button>
            </form>
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
    name: 'AddPet',
    data() {
        return {
            username: '',
            userid: '',
            name: '',
            age: '',
            gender: '',
            breed: '',
        };
    },
    created() {
        this.username = localStorage.getItem('username');
        this.userid = localStorage.getItem('userid');
    },
    methods: {
        async submitForm() {
            const formData = {
                name: this.name,
                age: this.age,
                breed: this.breed,
                gender: this.gender,
                owner_id: this.userid,
            };

            try {
                axios.post('http://127.0.0.1:8000/api/v1/owner/add_pet', formData)
                    .then(response => {
                        console.log('Pet Added:', response.data);
                        window.alert('Pet Added successfully !!!');
                        this.$router.push({ name: 'HomePage' })
                    })
                    .catch(error => {
                        console.warn('Adding Pet failed:', error.response.data);
                    });
            } catch (error) {
                console.error('Adding Pet failed:', error.response.data);
            }
        },
    },
};
</script>