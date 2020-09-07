// innerHTML += createPostItem("/posts/images/"+id+"/"+id+".jpg", title, "/posts/categories/"+category+"/"+id+".html", keyword);
$(document).ready(function () {
    var keywords = getkeywords();
    if (keywords.length) {
        getIds(keywords).done((val)=> {
            if (val.length) {
                var sortedIds = sortIds(val);  
                var innerHTML = "<h3>Related Posts</h3>\n<ul>"
                $.each(sortedIds, (i, data)=> {
                    var img_loc = "/posts/images/"+data.id+"/"+data.id+".jpg";
                    var title = data.title;
                    var link = "/posts/categories/"+data.category+"/"+data.id+".html";
                    var keyword = data.keyword;
                    var date = $('#post-date').text();
                    innerHTML += createPostItem(img_loc, title, link, keyword, date);
                });
                innerHTML += "</ul>"
                $('#related-posts').html(innerHTML);  
            } else {
               $('#related-posts').addClass("d-none");
            }
        });
    }
});

function getkeywords() {
    var keywordsTags = $('.tag-list').children(".badge");
    keywords = []
    $(keywordsTags).each(function (index, keywordsTag) {
        keywords.push($(keywordsTag).text());
    });
    return keywords;
}

// search algorithm
function getIds(words) {
    var def = $.Deferred();
    var ids = [];
    $.getJSON("/posts/search.json").done(function(json) {
        $.each(words, function (index, word) { 
            $.each(json.posts, (i, val) => {
                // making the array for searching keywords
                var tempList = [val.title];
                tempList = tempList.concat(val.keywords);
    
                // make a searchable object
                dict = FuzzySet(tempList, false);
                // search keyword
                res_list = dict.get(word);
    
                res = resultWithHighScore(res_list);
    
                if (res) {
                    if (!existAlready(val.id, ids)) {
                        var thisId = $('#post-id').attr("post-id");
                        if (thisId != val.id) {
                            ids.push({
                                "id":val.id,
                                "keyword":res[1],
                                "title":val.title,
                                "category":val.category
                            });
                        }
                    }
                } 
            });
        });
        def.resolve(ids);
    });
    return def
}

// find result with high score
function resultWithHighScore(res_list) {
    if (res_list) {
        var high_res = [0.34, ""];
        $.each(res_list, (i, res) => {
            if (res[0] > high_res[0]) {
                high_res = res;
            }
        });
        return high_res;
    } else {
        return null;
    }           
}

function sortIds(ids) {
    var tempId;

    for (let i = 0; i < ids.length; i++) {             
        for (let j = i+1; j < ids.length; j++) {
            if (ids[i][1] < ids[j][1]) {
                tempId = ids[i];
                ids[i] = ids[j];
                ids[j] = tempId;
            }
        }
    }
    return ids;
}

if (!String.prototype.format) {
    String.prototype.format = function() {
      var args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) { 
        return typeof args[number] != 'undefined'
          ? args[number]
          : match
        ;
      });
    };
}

function createPostItem(img_loc, title, link, keyword, date) {
    var htmlString = `
    <li>
        <div class="sidebar-thumb">
            <div class="img-post wow rollIn d-flex justify-content-center">
                <img src="{0}" alt="{1}" />
            </div>
        </div>
        <!-- .Sidebar-thumb -->
        <div class="sidebar-content">
            <h5 class="animated bounceInRight"><a href="{2}">{1}</a></h5>
        </div>
        <!-- .Sidebar-thumb -->
        <div class="sidebar-meta">
            <span class="time"><i class="far fa-clock"></i>{4}</span><br>
            <span class="badge badge-secondary p-1" style="color:aliceblue; font-weight: bolder;">{3}</span>
        </div>
        <!-- .Sidebar-meta ends here -->
    </li>\n`;
    
    return htmlString.format(img_loc, title, link, keyword, date);
}

function existAlready(postId, ids) {
    var e = false;
    $.each(ids, function (i, id) {
         if (postId == id['id']) {
            e = true;
         }
    });
    return e;
}