var category = "";
$(document).ready(() => {
    var url = window.location.href;
    var data = url.split("?")[1].split("=")[1];
    category = data;
    if ($('.post-list').length) { // check if post is available in the page
        $('.post-list').load(name + "posts/post-cards.html", function () {
            $('.post-list').children(":not([category="+category+"])").remove();
            $('#home h1').text(category.replace("-"," "));
            var items = $('.post-list').find("[category="+category+"]");
            console.log(items.length);
            $.each(items, (i, item) => {
                var tag = $(item).find("[href]");
                var img_tag = $(item).find(".image");
                var id = $(item).attr("id-number");
                $(tag).attr("href", "/posts/categories/"+category+"/"+id+".html");
                $(img_tag).attr("style", "background-image: url('/posts/images/"+id+"/"+id+".jpg');");
            });
            var pageNumber = 1;
            var perPage = 6;
            showPage(pageNumber, perPage);
            setPagination(
                pageNumber,
                perPage
            );
        });
    }
});

function paginationClicked(pageNumber) {
    var perPage = 6;
    showPage(pageNumber, perPage);
    setPagination(pageNumber,perPage);

    $('html, body').stop().animate({ scrollTop:  $('#posts').offset().top }, "slow");
}

function setPagination(pageNumber, perPage) {
    var pages = formatPage(pageNumber, perPage);
    var numberTag = '';
    var extraTag = '<li class="page-item"><a>&hellip;</a></li>\n';
    var totalPages = Math.ceil($('.post-list').children().length/perPage);
    var nextTag = '';
    var prevTag = '';
    if(pageNumber!=totalPages){
        nextTag = '<li class="page-item"><a class="page-link"  onclick="paginationClicked('+(pageNumber+1)+')" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>\n';
    }
    if(pageNumber!=1){
        prevTag = '<li class="page-item"><a class="page-link"  onclick="paginationClicked('+(pageNumber-1)+')" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>\n';
    }
    pages.forEach(function (page) {
        if (page == '.') {
            numberTag += extraTag;
        } else if (parseInt(page) == pageNumber) {
            numberTag += '<li class="page-item active"><a class="page-link" onclick="paginationClicked('+page+')">' + page + '</a></li>\n';
        } else {
            numberTag += '<li class="page-item"><a class="page-link" onclick="paginationClicked('+page+')">' + page + '</a></li>\n';

        }
    });
    var html = prevTag + numberTag + nextTag
    $("#posts").find(".pagination").html(html)
}

function showPage(pageNumber, perPage) {
    var items = $('.post-list').find("[category="+category+"]");
    var numItems = items.length;
    var showFrom = perPage * (pageNumber-1);
    var showTo = showFrom + perPage;
    items.hide().slice(showFrom, showTo).show();
}

function formatPage(pageNumber, perPage){
    var totalPages = Math.ceil($('.post-list').children().length/perPage);
    var first = 1;
    var last = totalPages;
    if (totalPages<=7){
        return makeList(first, last);
    }
    if(first<=pageNumber && pageNumber<(first+2)){
        var fList = makeList(first, pageNumber+1);
        var mList = [".",String(Math.floor(last/2)),"."];
        fList = fList.concat(mList);
        var remaining = 7-fList.length;
        var lList = makeList(last-remaining+1, last);
        fList = fList.concat(lList);
        return fList
    }else if(pageNumber==(first+2)){
        var fList = makeList(first, pageNumber+1);
        var mList = ["."];
        fList = fList.concat(mList);
        var remaining = 7-fList.length;
        var lList = makeList(last-remaining+1, last);
        fList = fList.concat(lList);
        return fList
    }else if((first+2)<pageNumber && pageNumber<(last-2)){
        var fList = [String(first),".",String(pageNumber-1),String(pageNumber),String(pageNumber+1),".",String(last)];
        return fList
    }else if(pageNumber==(last-2)){
        var lList = makeList(pageNumber-1, last);
        var mList = ["."];
        mList = mList.concat(lList);
        var remaining = 7-mList.length;
        var fList = makeList(first, remaining);
        fList = fList.concat(mList);
        return fList
    }else if((last-2)<pageNumber && pageNumber<=last){
        var lList = makeList(pageNumber-1, last);
        var mList = [".",String(Math.floor(last/2)),"."];
        mList = mList.concat(lList);
        var remaining = 7-mList.length;
        var fList = makeList(first, remaining);
        fList = fList.concat(mList);
        return fList
    }
}

function makeList(from, to){
    var l = []
    for(i=from;i<=to;i++){
        l.push(String(i));
    }
    return l;
}