<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Doggys Day </h1>
        </div>
        <div class="content-container">
            <form class="form-container">
                <h2 class="signup-title">Owner Sign Up</h2>
                <div class="input-field">
                    <input type="email" placeholder="Email" v-model="email" required />
                </div>
                <div class="input-field">
                    <input type="tel" placeholder="Phone Number" v-model="phoneNumber" required />
                </div>
                <div class="input-field">
                    <input type="password" placeholder="Password" v-model="password" required />
                </div>
                <div class="input-field">
                    <input type="password" placeholder="Confirm Password" v-model="confirmPassword" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Name" v-model="username" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Address" v-model="address" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Latitude" v-model="latitude" required />
                </div>
                <div class="input-field">
                    <input type="text" placeholder="Longitude" v-model="longitude" required />
                </div>
                <!-- <button class="signup-button" type="submit" @click="submitForm">Submit</button> -->
                <button class="signup-button" type="submit" :disabled="isFormInvalid" @click="submitForm">Submit</button>
            </form>
        </div>

    </div>
</template>
  
<script>
import './styles.css';
import axios from 'axios';

export default {
    name: 'OwnerSignUp',
    data() {
        return {
            username: '',
            password: '',
            confirmPassword: '',
            email: '',
            phoneNumber: '',
            address: '',
            latitude: '',
            longitude: '',
        };
    },
    computed: {
        isFormInvalid() {
            return (
                !this.username ||
                !this.password ||
                !this.confirmPassword ||
                !this.email ||
                !this.phoneNumber ||
                !this.address ||
                !this.latitude ||
                !this.longitude ||
                !this.isEmailValid() ||
                !this.isPhoneValid() ||
                !this.checkPassword()
            );
        },
    },
    methods: {
        isEmailValid() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(this.email);
        },
        isPhoneValid() {
            if (this.phoneNumber.length == 10) {
                return true;
            }
            return false;
        },
        checkPassword() {
            if (this.confirmPassword == this.password) {
                return true;
            }
            return false;
        },
        async submitForm() {
            const formData = {
                name: this.username,
                password: this.password,
                //   confirmPassword: this.confirmPassword,
                email: this.email,
                phone: this.phoneNumber,
                address: this.address,
                lat: this.latitude,
                lon: this.longitude,
            };

            try {
                axios.post('http://127.0.0.1:8000/api/v1/owner/signup', formData)
                    .then(response => {
                        console.log('Logged in:', response.data);
                        window.alert('Account created successfully !!!');
                        window.location.href = '/signin';
                    })
                    .catch(error => {
                        console.warn('Login failed:', error.response.data);
                    });
            } catch (error) {
                console.error('Sign up failed:', error.response.data);
                this.errorMessage = 'Error occurred while signing up.';
            }
        },
    },
};
</script>

  