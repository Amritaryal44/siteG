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

$(document).ready(function () {
    // ToolTip initialization
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').attr("data-placement", "top");
 });

// for category list
$(function() {
    $.contextMenu({
        selector: '.category-item a', 
        callback: function(key, options) {
            if (key == "rename") {
                $(this).siblings('.rename-modal').modal('show');
                var inputField = $(this).siblings(".rename-modal").find("input[type='text']");
                $(this).siblings('.rename-modal').on('shown.bs.modal', function () {
                    $(inputField).trigger('focus');
                })
            } else if (key == "delete") {
                if (confirm("Are you sure?")) {
                    var categoryName = $(this).children(".category-name").text().trim().toLowerCase();
                    $.ajax('/post-section/', {
                        type: 'POST', 
                        data: { submit: 'delete',  name: categoryName },
                        success: function (response) {
                            window.location.href = "/post-section/";
                        }
                    });
                }
            }
        },
        items: {
            "rename": {name: "Rename", icon: "fas fa-edit"},
            "delete": {name: "Delete", icon: "fas fa-trash-alt"},
        }
    }); 
});
 
$('.add-category').click(function (e) { 
    var modal = $(e.target).siblings('#add-modal');
    $(modal).modal('show');
    var inputField = $(modal).find("input[type='text']");
    $(modal).on('shown.bs.modal', function () {
        $(inputField).trigger('focus');
    });
});

// for post list
$(function() {
    $.contextMenu({
        selector: '.list-group-item', 
        callback: function(key, options) {
            if (key == "rename") {
                $(this).siblings('.rename-modal').modal('show');
                var inputField = $(this).siblings(".rename-modal").find("input[type='text']");
                $(this).siblings('.rename-modal').on('shown.bs.modal', function () {
                    $(inputField).trigger('focus');
                })
            } else if (key == "delete") {
                if (confirm("Are you sure?")) {
                    var postId = $(this).attr("id").split("-")[1].trim();
                    var categoryName = $("#category-name h1").text().split(" - ")[1].trim().toLowerCase().replaceAll(" ", "-");
                    $.ajax('/post-section/'+categoryName+"/", {
                        type: 'POST', 
                        data: { submit: 'delete',  id: postId },
                        success: function (response) {
                            window.location.href = "/post-section/"+categoryName;
                        }
                    });
                }
            }
        },
        items: {
            "rename": {name: "Rename", icon: "fas fa-edit"},
            "delete": {name: "Delete", icon: "fas fa-trash-alt"},
        }
    });   
});
 
$('.add-post').click(function (e) { 
    var modal = $(e.target).siblings('#add-modal');
    $(modal).modal('show');
    var inputField = $(modal).find("input[type='text']");
    $(modal).on('shown.bs.modal', function () {
        $(inputField).trigger('focus');
    });
});

function loadFile(event) {
    console.log(URL.createObjectURL(event.target.files[0]), "is file");
    img = $(event.target).parent().siblings("div").find("img");
    $(img).attr("src", URL.createObjectURL(event.target.files[0]));
}

function allowDrop(ev) {
    ev.preventDefault();
    $('.upload-item').addClass('drag-controlled');
}
  
function drop(ev) {
    ev.preventDefault();
    $('.upload-item').removeClass('drag-controlled');
    uploadImage(ev.dataTransfer.files[0]);
}

function uploadImage(file) { 
    var formData = new FormData();
    formData.append('submit', 'upload');
    formData.append('image', file);
    var urlDat = document.location.href;
    $.ajax({
        type: "post",
        url: urlDat,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $('.image-list').html(imageHTML(response));
        }
    });
}

$(document).on('click', '.img-delete', function (e) {
    var formData = new FormData();
    var imgId = $(e.target).attr('name');
    var imgFormat = $(e.target).attr('format');
    formData.append('submit', 'delete');
    formData.append('id', imgId);
    formData.append('format', imgFormat);
    $.ajax({
        type: "post",
        url: document.location.href,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $(e.target).parents()[2].remove();
        }
    });
});

function imageHTML(response){
    var cards = "";
    $($('.image-list').children('.card')).each(function (index, card) {
        preTag = '<div class="card m-3">';
        postTag = '</div>';
        cards+=preTag+$(card).html()+postTag;
    });
    htmlData = '<div class="card m-3">\
        <div class="card-body p-0">\
            <div class="image-item img-fluid" style="background-image: url(/posts/images/{1}/{1}-{2}.{3});">\
                <button class="img-delete close p-2" aria-label="Close" type="submit" name="{2}" format="{3}">\
                    &times;\
                </button>\
            </div>\
        </div>\
        <div class="card-footer pb-0">\
            <p>/posts/images/{1}/{1}-{2}.{3}</p>\
        </div>\
    </div>';
    htmlData = htmlData.format(response['category'], response['postId'], response['imgId'], response['imgFormat']);
    cards+=htmlData;
    preTag = '<div class="upload-item image-item m-3 d-flex flex-column justify-content-center" style="border: dashed 1px black;" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="$(\'.upload-item\').removeClass(\'drag-controlled\');">';
    postTag = '</div>'
    cards+=preTag+$('.image-list').children('.upload-item').html()+postTag;
    return cards;
}

$('#post-setup').submit(function (e) { 
    e.preventDefault();
    
    var formData = new FormData(this);
    formData.append('submit', 'Save');
    $.ajax({
        type: "post",
        url: document.location.href,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            $('#post-name h1').text(formData.get('title'));
            $('.back-button').attr("href", '/post-section/'+formData.get('category')+'/');
            var newUrl = '/post-section/'+formData.get('category')+'/'+response['postId']+'/';
            window.history.pushState({"html":document.html,"pageTitle":document.title},"", newUrl);
        }
    });
});

$('#post-date').change(function (e) { 
    e.preventDefault();

    if ($(this).val()) {
        if (confirm("Are you sure?")) {
            var formData = new FormData();
            formData.append('submit', 'date');
            formData.append('date', $(this).val());
            $.ajax({
                type: "post",
                url: document.location.href,
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
        
                }
            });
        }
    }
});