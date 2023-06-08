<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ username }}</h1>
        </div>

        <div class="content-container">
            <h2>Nearby Caretakers:</h2>
            <div class="inner-container">
                <div class="small-container caretaker-item" v-for="item in receivedData" :key="item.id"
                    @click="handleClick(item.id, item.name)">
                    <p>{{ item.name }}</p>
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
    console.warn(config);
    return config;
});

export default {
    name: 'FindCaretaker',
    data() {
        return {
            username: '',
            receivedData: '',
            responseData: '',
        }
    },
    created() {
        this.username = localStorage.getItem('username');
        this.userid = localStorage.getItem('userid');
        this.receivedData = JSON.parse(this.$route.params.responseData)
    },
    methods: {
        handleClick(caretaker_id, caretaker_name) {
            const formData = {
                id: caretaker_id
            };
            try {
                axios.get(`http://127.0.0.1:8000/api/v1/caretaker/${caretaker_id}`, { params: formData })
                    .then(response => {
                        console.log('Caretaker Info:', response.data);
                        this.$router.push({
                            name: 'CaretakerInfo', params: {
                                caretaker_id: caretaker_id,
                                caretaker_name: caretaker_name,
                                responseData: JSON.stringify(response.data)
                            }
                        })
                    })
                    .catch(error => {
                        console.warn('Fetching Caretaker Info Failed:', error.response.data);
                    });
            }
            catch (error) {
                console.warn('Fetching Caretaker Info Failed:', error.response.data);
            }
        }
    }
};
</script>