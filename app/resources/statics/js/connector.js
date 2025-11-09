const { createApp } = Vue
const app = createApp({
    data() {
        let connectorList = [];
        let selectConnector = {
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
            connectorList,
            selectConnector
        }
    },
    created() {
        this.connectorList = [
            {
                id: 'uuid1',
                name: 'N-ISAC',
                url: 'https://fake.domain/path',
                api_token: 'qjwierjiosdajfoisdaf',
                enabled: true,
                confidence: 5,
                tag: 'N-ISAC',
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
        editConnector(uuid) {
            this.selectConnector = this.connectorList.find((ele) => uuid === ele.id);

        },
        onSwitchActive(item){
        }

    }
}).mount('#vue-app-connector-id');