$(document).ready(function () {
    var searchWord = getSearchWord();
    if (searchWord != -1) {
        var ids = getIds(searchWord).done((val)=> {
            var innerHTML = "";
            if (val.length) {
                var sortedIds = sortIds(val);
                if (sortedIds.length == 1) {
                    innerHTML = '<p class="search-results-count">About '+sortedIds.length+' result found</p>';
                } else {
                    innerHTML = '<p class="search-results-count">About '+sortedIds.length+' results found</p>';
                }
                
                $.each(sortedIds, (i, data)=> {
                    var id = data[0];
                    var score = data[1];
                    var keyword = data[2];
                    var title = data[3];
                    var description = data[4];
                    var category = data[5];
                    var link = "/posts/categories/"+category+"/"+id+".html";
                    innerHTML += createSearchItem("/posts/images/"+id+"/"+id+".jpg", title, keyword, score, description, link);
                });    
            } else {
                innerHTML = "<h2 class='text-center'>Sorry, No result found!!!</h2>";
            }
            $('#search-result').html(innerHTML);
        });
    }
});

function getSearchWord() {
    var url = window.location.href;
    if ((url.search(/[?]/g) && url.search("=") != -1)) {
        return url.split("?")[1].split("=")[1].replace("+", " ");
    } else {
        return -1;
    }
}

// search algorithm
function getIds(word) {
    var ids = [];
    var def = $.Deferred();

    $.getJSON("/posts/search.json", async function(json) {
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
                ids.push([val.id].concat(res).concat([val.title, val.description, val.category]));
            } 
        });
        def.resolve(ids);
    });

    return def;
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

function createSearchItem(img_loc, title, keyword, score, description, link) {
    var htmlString = `<section class="search-result-item">
    <a class="image-link" href="#"><span class="image" style="background-image: url({0});"></span>
    </a>
    <div class="search-result-item-body">
        <h4 class="search-result-item-heading"><a href="{4}">{1}</a></h4>
        <p class="info">{2}</p>
        <p class="description">{3}</p>
    </div>
</section>`;
    
    return htmlString.format(img_loc, title, "Matched "+parseInt(score*100)+"% with keyword "+keyword, description, link);
}