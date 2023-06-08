<template>
  <div class="page-container">
    <div class="header-container">
      <h1> Doggys Day </h1>
    </div>
    <div class="content-container">
      <div class="left-section">
        <div class="image-container">
          <img class="background-logo" src="../assets/doggys_day_landscape.png" />
        </div>
      </div>
      <div class="right-section">
        <div class="image-container">
          <img class="logo" src="../assets/dog.png" />
        </div>
        <form class="form-container">
          <h2 class="login-title">User Login</h2>
          <div class="input-field">
            <input type="text" placeholder="Email/Mobile" required v-model="username" />
          </div>
          <div class="input-field">
            <input type="password" placeholder="Password" required v-model="password" />
          </div>
          <button class="login-button" type="submit" @click="login">Login</button>
          <p class="new-user-text">New user?</p>
          <button class="signup-button" type="button" @click="signup()">Sign Up</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import './styles.css';
import axios from 'axios';

export default {
  name: 'SignIn',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      try {
        const formData = {
          username: this.username,
          password: this.password,
        };
        axios.post('http://127.0.0.1:8000/api/v1/authentication/owner_login', formData)
          .then(response => {
            console.log('Logged in:', response.data);
            this.responseData = response.data
            // const name = response.data.name;
            // const responseData = JSON.stringify(response.data);
            // const redirectURL = `/home?data=${encodeURIComponent(responseData)}`;
            // window.location.href = redirectURL;
            this.$router.push({ name: 'HomePage', params: { name: this.responseData.name, id: this.responseData.id } })
            // const { access_token, refresh_token } = response.data;
            // localStorage.setItem('access_token', access_token);
            // localStorage.setItem('refresh_token', refresh_token);
          })
          .catch(error => {
            console.warn('Login failed:', error.response.data);
          });
      }
      catch (error) {
        console.warn('Login failed:', error.response.data);
      }
      this.username = '';
      this.password = '';
    },

    signup() {
      this.$router.push({ name: 'SignUp' })
    }
  }
};
</script>


