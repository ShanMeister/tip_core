const { createApp } = Vue
const app = createApp({
    data() {

        return {
        }
    },
    created() {

    },
    methods: {
        back() {
            history.back();
        },
    

    }
}).mount('#vue-app-login-id');