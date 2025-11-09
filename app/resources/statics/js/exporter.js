const { createApp } = Vue
const app = createApp({
    data() {
        let exporterList = [];
        let selectExporter = {
            id: '',
            name: '',
            api_token: '',
            status_info: {}
        };
        return {
            exporterList,
            selectExporter
        }
    },
    created() {
        this.exporterList = [
            {
                id: 'uuid1',
                name: '普藍地',
                api_token: 'qjwierjiosdajfoisdaf',
                // 查詢最近是否有失敗，若有失敗則觀看紀錄。(exporter會打API回來表示成功)
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
        editExporter(uuid) {
            this.selectExporter = this.exporterList.find((ele) => uuid === ele.id);

        },

    }
}).mount('#vue-app-exporter-id');