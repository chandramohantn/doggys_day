<template>
    <div class="page-container">
        <div class="header-container">
            <h1>Welcome {{ username }}</h1>
        </div>

        <div class="content-container">
            <h2>Pet Info:</h2>
            <ul>
                <li v-for="item in receivedData" :key="item.id">{{ item.name }}, {{ item.age }}, {{ item.gender }}, {{
                    item.breed }}</li>
            </ul>
        </div>
    </div>
</template>


<script>
import './styles.css';

export default {
    name: 'PetInfo',
    data() {
        return {
            username: '',
            receivedData: ''
        }
    },
    created() {
        this.username = localStorage.getItem('username');
        this.receivedData = JSON.parse(this.$route.params.responseData)
    },
};
</script>