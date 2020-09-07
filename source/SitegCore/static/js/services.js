$(document).ready(function () {
    // script to load when document is ready
    
 });
 
 function loadFile(event) {
    img = $(event.target).parent().siblings("div").find("img");
    $(img).attr("src", URL.createObjectURL(event.target.files[0]));
 }

 $('.delete').click(function (e) { 
    if (confirm("Are you sure?")) {  
        myData = $(e.target).attr("name");

        $.ajax('/service-section/', {
            type: 'POST', 
            data: { submit: 'Delete',  service: myData },
            success: function (response) {
                window.location.href = "/service-section/"
            }
        });
    }
 });
 
 