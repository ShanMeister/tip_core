const { createApp } = Vue
const app = createApp({
    data() {
        let blackList = [];
        let selectBlack = {
            id: '',
            name: '',
            tag: '',
            source: '',
            created_date: '',
            update_dated: '',
            author: '',
            description: '',
        };
        let advanceSearch ={
            'radio_filter':{
                'all': true,
                'ip': true,
                'domain': true,
                'url': true
            }
        }
        let tagList = ['cve', 'N-ISAC']

        return {
            blackList,
            selectBlack,
            advanceSearch,
            tagList
        }
    },
    created() {
        this.blackList = [
            {
                id: 'uuid1',
                name: '10.10.10.10',
                tag: 'N-ISAC',
                source: 'N-ISAC',
                created_date: '2024-05-15 00:00:00',
                update_dated: '2024-05-15 00:00:00',
                author: 'xing',
                description: '鑑識到的可怕黑名單'
            }

        ]
    },
    methods: {
        back() {
            history.back();
        },
        filevalidation(){

            return true;
        }
    },
    watch: {
        'advanceSearch.radio_filter.all' :function (newValue, oldValue) {
        
        },
        'advanceSearch.radio_filter.ip' :function (newValue, oldValue) {
        
        },
        'advanceSearch.radio_filter.domain' :function (newValue, oldValue) {
        
        },
        'advanceSearch.radio_filter.url' :function (newValue, oldValue) {
        
        },
    }
}).mount('#vue-app-intelligence-id');