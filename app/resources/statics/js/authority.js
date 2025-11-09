const { createApp } = Vue
const app = createApp({
    data() {
        let authorityList = [];
        let selectAuthorityList = {
            key: '',
            authority: '',
            valid_from: '',
            expiration_date: '',
            note: '',
            enabled: ''
        };
        let newAuthorityList = [];
        let selectNewAuthorityList = {
            key: '',
            authority: '',
            valid_from: '',
            expiration_date: '',
            note: '',
        };
        let tagList = ['cve', 'N-ISAC']

        return {
            authorityList,
            selectAuthorityList,
            newAuthorityList,
            selectNewAuthorityList,
            tagList
        }
    },
    created() {
        this.authorityList = [
            {
                key: 'xyzabc',
                authority: 'whois',
                valid_from: '2024-03-01',
                expiration_date: '2024-04-30',
                note: '權限說明',
                enabled: true
            }
        ]
    },
    methods: {
        back() {
            history.back();
        },
        editAuthorityList(uuid) {
            this.selectAuthorityList = this.authorityList.find((ele) => uuid === ele.id);

        }
    }
}).mount('#vue-app-authority-id');