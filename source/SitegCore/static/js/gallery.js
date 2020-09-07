$(document).ready(function () {
    // script to load when document is ready
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="tooltip"]').attr("data-placement", "top");
 });

 $('.delete').click(function (e) { 
    if (confirm("Are you sure?")) {  
        myData = $(this).attr("name");
        $.ajax('/gallery-section/', {
            type: 'POST', 
            data: { submit: 'delete',  service: myData },
            success: function (response) {
                window.location.href = "/gallery-section"
            }
        });
    }
 });
 
 