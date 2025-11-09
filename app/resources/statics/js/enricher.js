const { createApp } = Vue
const app = createApp({
    data() {
        let enricherList = [];
        let selectEnricher = {
            id: '',
            name: '',
            url: '',
            api_token: '',
            enabled: '',
            confidence: '',
            tag: '',
            retry_count: '',
            status_info: {}
        };
        return {
            enricherList,
            selectEnricher
        }
    },
    created() {
        this.enricherList = [
            {
                id: 'uuid1',
                name: 'WHOIS',
                url: 'https://fake.domain/path',
                api_token: 'qjwierjiosdajfoisdaf',
                enabled: true,
                confidence: 5,
                tag: 'WHOIS',
                retry_count: 3,
                status_info: {
                    timestamp: new Date(),
                    status: 'good'
                }
            }

        ]
    },
    methods: {
        back() {
            history.back();
        },
        editEnricher(uuid) {
            this.selectEnricher = this.enricherList.find((ele) => uuid === ele.id);

        },
        onSwitchActive(item){
        }

    }
}).mount('#vue-app-enricher-id');