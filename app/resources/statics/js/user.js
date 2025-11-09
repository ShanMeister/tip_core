const { createApp } = Vue
const app = createApp({
    data() {
        let userList = [];
        let selectUserList = {
            email: '',
            authority: '',
            enable: '',
            active: '',
        };
        let newUserList = [];
        let selectNewUserList = {
            email: '',
            authority: '',
        };
        return {
            userList,
            selectUserList,
            newUserList,
            selectNewUserList
        }
    },
    created() {
        this.userList = [
            {
                email: 'xyz@chtsecurity.com',
                authority: 'root',
                enabled: true,
                active: 'True'
            }
        ]
    },
    methods: {
        back() {
            history.back();
        },
        editYararuleList(uuid) {
            this.selectUserList = this.userList.find((ele) => uuid === ele.id);

        },
        onSwitchEnable(item){
        },
        onSwitchActive(item){
        },
        inputNewUser(item){
        }
    }
}).mount('#vue-app-user-id');