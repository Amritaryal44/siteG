$(document).ready(function () {
   // script to load when document is ready
   var checkBoxs = $('input[type="checkbox"]')
   $.each(checkBoxs, function (index, checkBox) { 
      if (!$(checkBox).prop("checked")) {
         var inputField = $(checkBox).parent().parent().siblings("input");
         $(inputField).prop("disabled", true);
      }
   });
});

function loadFile(event) {
   console.log(URL.createObjectURL(event.target.files[0]), "is file");
   img = $(event.target).parent().siblings("div").find("img");
   $(img).attr("src", URL.createObjectURL(event.target.files[0]));
}

$('input[type="checkbox"]').change(function (e) { 
   e.preventDefault();
   var inputField = $(this).parent().parent().siblings("input");
   if ($(e.target).prop("checked")) {
      $(inputField).prop("disabled", false);
   } else {
      $(inputField).prop("disabled", true);
   }
});
