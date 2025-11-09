const { createApp } = Vue
const app = createApp({
    delimiters: ['[[',']]'],
    data() {
        let yararuleList = [];
        let selectYararuleList = {
            name: '',
            tag: '',
            author: '',
            rule: '',
            created_date: '',
        };
        let inputYararuleList = [];
        let selectInputYararuleList = {
            rule: '',
        };
        let yaraPaging = new PaginatorTip({
            search_text: '',
            category: ''
        }, 10);
        let tagList;
        return {
            yararuleList,
            selectYararuleList,
            inputYararuleList,
            selectInputYararuleList,
            yaraPaging,
            tagList
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
                url: '/yara_rule/list/',
                type: 'SEARCH',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(this.yaraPaging.genRequest()),
                beforeSend: () => {
                    ui.Loading.start();
                }
            }).done((res) => {
                this.yaraPaging.setPaging(res);
            }).always(() => {
                ui.Loading.stop();
            });
        },
        searchPage(clickPage) {
            this.yaraPaging.paging.current_page = clickPage;
            this.getDataOnSearch();
        },
        updatePage(pageNumber) {
            this.yaraPaging.paging.current_page += pageNumber;
            this.getDataOnSearch();
        },
        isDisplayPaging(renderPageNumber) {
            return this.yaraPaging.isDisplayPaging(renderPageNumber)
        },
        editYararuleList(uuid) {
            this.selectYararuleList = this.yararuleList.find((ele) => uuid === ele.id);
        },
        onDeleteRule(ruleID, ruleName) {
            ui.dialog(`是否要刪除「${ruleName}」標籤?`).confirm(() => {
                $.ajax({
                    url: '/yara_rule/view/',
                    type: 'DELETE',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({ id: ruleID }),
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
}).mount('#vue-app-yararule-id');