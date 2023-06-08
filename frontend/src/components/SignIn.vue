<template>
  <div class="page-container">
    <div class="header-container">
      <h1>Welcome {{ username }}</h1>
    </div>

    <div class="content-container">
      <div class="inner-container">
        <div class="small-container card-container">
          <p>Owner</p>
          <form class="form-container">
            <h2 class="login-title">Owner Login</h2>
            <div class="input-field">
              <input type="text" placeholder="Email/Mobile" required v-model="username" />
            </div>
            <div class="input-field">
              <input type="password" placeholder="Password" required v-model="password" />
            </div>
            <button class="login-button" type="submit" @click="owner_login">Signin</button>
            <p class="new-user-text">New Owner?</p>
            <button class="signup-button" type="button" @click="owner_signup()">Sign Up</button>
          </form>
        </div>
        <div class="small-container card-container">
          <p>Caretaker</p>
          <form class="form-container">
            <h2 class="login-title">Caretaker Login</h2>
            <div class="input-field">
              <input type="text" placeholder="Email/Mobile" required v-model="username" />
            </div>
            <div class="input-field">
              <input type="password" placeholder="Password" required v-model="password" />
            </div>
            <button class="login-button" type="submit" @click="caretaker_login">Signin</button>
            <p class="new-user-text">New Caretaker?</p>
            <button class="signup-button" type="button" @click="caretaker_signup()">Sign Up</button>
          </form>
        </div>
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
      access_token: '',
      refresh_token: '',
      token_type: '',
    };
  },
  methods: {
    store_user_info(user_info) {
      localStorage.setItem('username', user_info.name);
      localStorage.setItem('userid', user_info.id);
      localStorage.setItem('access_token', user_info.access_token);
      localStorage.setItem('refresh_token', user_info.refresh_token);
      localStorage.setItem('token_type', user_info.token_type);
    },
    owner_login() {
      try {
        const formData = {
          username: this.username,
          password: this.password,
        };
        axios.post('http://127.0.0.1:8000/api/v1/authentication/owner_signin', formData)
          .then(response => {
            console.log('Logged in:', response.data);
            this.store_user_info(response.data)
            this.$router.push({ name: 'HomePage' });
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
    owner_signup() {
      this.$router.push({ name: 'SignUp' });
    },
    caretaker_login() {
      try {
        const formData = {
          username: this.username,
          password: this.password,
        };
        axios.post('http://127.0.0.1:8000/api/v1/authentication/caretaker_signin', formData)
          .then(response => {
            console.log('Logged in:', response.data);
            this.store_user_info(response.data)
            this.$router.push({ name: 'HomePage' });
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
    caretaker_signup() {
      this.$router.push({ name: 'SignUp' })
    },
    // get_access_token() {
    //   const token_type = localStorage.getItem('token_type');
    //   token_type = token_type ? token_type : '';
    //   const access_token = localStorage.getItem('access_token');
    //   access_token = access_token ? access_token : '';
    //   return { 'token_type': token_type, 'access_token': access_token };
    // },
  },
};
</script>