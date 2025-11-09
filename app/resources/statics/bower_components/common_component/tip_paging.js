class PaginatorTip {

    constructor(searchFilter, page_size) {

        this.paging = {
            current_page: 1,
            page_size: page_size,
            total_item: 0,
            total_page: 0,
            items: {}
        };
        this.searchFilter = searchFilter;
    }


    isDisplayPaging(renderPageNumber){
        return Math.abs(renderPageNumber - this.paging.current_page) < 3 ||
                (this.paging.current_page < 3 && renderPageNumber < 6) ||
                (this.paging.current_page + 2 > this.paging.total_page && renderPageNumber + 5 > this.paging.total_page);
    }

    genRequest(){
        return {
            search: {
                ...this.searchFilter
            },
            paging: {
                current_page: this.paging.current_page,
                page_size: this.paging.page_size
            }
        };
    }

    setPaging(paging){
        this.paging = paging;
    }
};