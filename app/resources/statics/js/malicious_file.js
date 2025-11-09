const { createApp } = Vue
const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        let selectMaliciousFile = {
            file_name: '',
            file_hash: '',
            author: '',
            created_date: ''
        };
        let inputfileList = [];
        let selectInputfileList = {
            file_hash: '',
            file_name: '',
            file_tag: ''
        };
        let filePaging = new PaginatorTip({
            search_text: '',
            category: ''
        }, 10);
        return {
            inputfileList,
            selectInputfileList,
            selectMaliciousFile,
            filePaging
        }
    },
    created() {
        this.reload();
    },
    methods: {
        back() {
            history.back();
        },

        reload() {
            this.getDataOnSearch();
            this.getCategory();
        },
        getCategory() {
            let _this = this;
            $.getJSON('/tag/category', function (res) {
                if (res) {
                    _this.tagList = res.category;
                }
            });
        },
        getDataOnSearch() {
            $.ajax({
                url: '/malicious_file/list',
                type: 'SEARCH',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(this.filePaging.genRequest()),
                beforeSend: () => {
                    ui.Loading.start();
                }
            }).done((res) => {
                this.filePaging.setPaging(res);
            }).always(() => {
                ui.Loading.stop();
            });
        },
        searchPage(clickPage) {
            this.filePaging.paging.current_page = clickPage;
            this.getDataOnSearch();
        },
        updatePage(pageNumber) {
            this.filePaging.paging.current_page += pageNumber;
            this.getDataOnSearch();
        },
        isDisplayPaging(renderPageNumber) {
            return this.filePaging.isDisplayPaging(renderPageNumber)
        },
        onSaveMaliciousFile() {
            $.ajax({
                url: '/malicious_file/',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(this.selectInputfileList),
                beforeSend: () => {
                    ui.Loading.start();
                }
            }).done((res) => {
                this.reload();
            }).fail((res) => {
                if (res?.responseJSON) {
                    ui.alert(res?.responseJSON.message);
                }
            }).always(() => {
                ui.Loading.stop();
                $(`#saveModal`).modal('hide');
            });
        },
        onDeleteFile(fileID, fileName) {
            ui.dialog(`是否要刪除「${fileName}」標籤?`).confirm(() => {
                $.ajax({
                    url: '/malicious_file/',
                    type: 'DELETE',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({ id: fileID }),
                    beforeSend: () => {
                        ui.Loading.start();
                    }
                }).done((res) => {
                    this.reload();
                }).fail((res) => {
                    if (res?.responseJSON) {
                        ui.alert(res?.responseJSON.message);
                    }
                }).always(() => {
                    ui.Loading.stop();
                });
            });
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const wordArray = CryptoJS.lib.WordArray.create(e.target.result);
                    const hash = CryptoJS.SHA256(wordArray).toString(CryptoJS.enc.Hex);
                    this.selectInputfileList.file_name = file.name;
                    this.selectInputfileList.file_hash = hash;
                    // this.selectMaliciousFile.file_size = file.size;
                };
                reader.readAsArrayBuffer(file);
            }
        }
    }
}).mount('#vue-app-maliciousfile-id');