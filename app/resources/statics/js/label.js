const { createApp } = Vue
const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
        let selectLabel = {
            name: '',
            tag: '',
            author: '',
            created_date: '',
            modify_date: ''
        };
        let labelPaging = new PaginatorTip({
            search_text: '',
            category: ''
        }, 10);
        let categoryList = [];

        return {
            labelPaging,
            selectLabel,
            categoryList,
        }
    },
    created() {
        this.reload();
    },
    methods: {
        reload() {
            this.getDataOnSearch();
            this.getCategory();
        },
        getCategory() {
            let _this = this;
            $.getJSON('/tag/category', function (res) {
                if (res) {
                    _this.categoryList = res.category;
                }
            });
        },
        getDataOnSearch() {
            $.ajax({
                url: '/tag/list',
                type: 'SEARCH',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(this.labelPaging.genRequest()),
                beforeSend: () => {
                    ui.Loading.start();
                }
            }).done((res) => {
                this.labelPaging.setPaging(res);
            }).always(() => {
                ui.Loading.stop();
            });
        },
        saveLabelModal(uuid) {
            if (uuid) {
                const label = this.labelPaging.paging.items.find((ele) => uuid === ele.id);
                this.selectLabel = JSON.parse(JSON.stringify(label));
            } else {
                this.selectLabel = {};
            }
        },
        searchPage(clickPage) {
            this.labelPaging.paging.current_page = clickPage;
            this.getDataOnSearch();
        },
        updatePage(pageNumber) {
            this.labelPaging.paging.current_page += pageNumber;
            this.getDataOnSearch();
        },
        isDisplayPaging(renderPageNumber) {
            return this.labelPaging.isDisplayPaging(renderPageNumber)
        },
        onSaveLabel() {
            $.ajax({
                url: '/tag/',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(this.selectLabel),
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
        onDeleteLabel(labelId, tagName) {
            ui.dialog(`是否要刪除「${tagName}」標籤?`).confirm(() => {
                $.ajax({
                    url: '/tag/',
                    type: 'DELETE',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({ id: labelId }),
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

        }
    }
}).mount('#vue-app-label-id');