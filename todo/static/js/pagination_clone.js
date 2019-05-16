$(document).ready(function(e){
    
    $('#pagination-clone').twbsPagination({
    totalPages: window.js_len_top_result,
    // the current page that show on start
    startPage: 1,

    // maximum visible pages
    visiblePages: window.js_len_top_result,

    initiateStartPageClick: true,

    // template for pagination links
    href: false,

    // variable name in href template for page number
    hrefVariable: '{{number}}',

    // Text labels
    first: 'First',
    prev: 'Previous',
    next: 'Next',
    last: 'Last',

    // carousel-style pagination
    loop: false,

    // callback function
    onPageClick: function (event, page) {
        $('.page-active-clone').removeClass('page-active-clone');
        $('#clonepage'+page).addClass('page-active-clone');
        setTimeout(function() {window["cloneOurEditor"+page].refresh();},1);
        setTimeout(function() {window["cloneTheirEditor"+page].refresh();},1);
        },

    // pagination Classes
    paginationClass: 'pagination',
    nextClass: 'next',
    prevClass: 'prev',
    lastClass: 'last',
    firstClass: 'first',
    pageClass: 'page',
    activeClass: 'active',
    disabledClass: 'disabled'

    });
    $('#pagination-bug').twbsPagination({
    totalPages: window.js_len_top_bug,
    // the current page that show on start
    startPage: 1,

    // maximum visible pages
    visiblePages: window.js_len_top_bug,

    initiateStartPageClick: true,

    // template for pagination links
    href: false,

    // variable name in href template for page number
    hrefVariable: '{{number}}',

    // Text labels
    first: 'First',
    prev: 'Previous',
    next: 'Next',
    last: 'Last',

    // carousel-style pagination
    loop: false,

    // callback function
    onPageClick: function (event, page) {
        $('.page-active-bug').removeClass('page-active-bug');
        $('#bugpage'+page).addClass('page-active-bug');
        setTimeout(function() {
            window["bugOurEditor"+page].refresh();
        },1);
        window.codeAmount = document.getElementsByClassName("bugOur");
        for (i = 1; i < codeAmount.length+1; i++) {
            window["bugOurEditor"+i].scrollIntoView({line: window.js_top_bug[i-1][1]+1, ch:1});
        }
        },

    // pagination Classes
    paginationClass: 'pagination',
    nextClass: 'next',
    prevClass: 'prev',
    lastClass: 'last',
    firstClass: 'first',
    pageClass: 'page',
    activeClass: 'active',
    disabledClass: 'disabled'

    });
});