const { createApp } = Vue

const app = createApp({
    delimiters: ['[[',']]'],
    data() {
        let selectLabel = {
            name: '',
            tag: '',
            rule_content: '',
        };
        let tagList = ['cve', 'N-ISAC']
        return {
            selectLabel,
            tagList
        }
    },
    methods: {
        saveYaraRule() {
            console.log("Saving Yara Rule:", this.selectLabel);
            const request = {
                name: this.selectLabel.name,
                tag: this.selectLabel.tag,
                rule_content: this.selectLabel.rule_content
            };

            $.ajax({
                url: '/yara_rule/view/',
                type: 'POST',
                data: JSON.stringify(request),
                contentType: 'application/json',
            }).done((res) => {
                // 使用 SweetAlert2 弹出成功提示
                Swal.fire({
                    title: '成功',
                    text: 'Yara rule 保存成功',
                    icon: 'success',
                    confirmButtonText: '確定'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // 重置表单
                        this.selectLabel.name = '';
                        this.selectLabel.tag = '';
                        this.selectLabel.rule_content = '';
                        // 跳转到其他页面
                        window.location.href = '/yara_rule/';
                    }
                });
            }).fail((res) => {
                if (res?.responseJSON) {
                    Swal.fire({
                        title: '錯誤',
                        text: res.responseJSON.message,
                        icon: 'error',
                        confirmButtonText: '確定'
                    });
                }
            }).always(() => {
                ui.Loading.stop();
            });
        },
    }
}).mount('#vue-app-yararule-update-id');