/*
    > credits for js libraries I used
        * wow.min.js from https://wowjs.uk/
        * pace.min.js from https://github.hubspot.com/pace/docs/welcome/
        * slick.min.js from https://kenwheeler.github.io/slick/
        * bootstrap.min.js from https://getbootstrap.com/
        * jquery-2.5.1.min.js from https://jquery.com/
*/

/* giving an awesome scroll effect */
var wow = new WOW({
    offset: 100,
});
wow.init();

$(document).ready(function() {
    /* adding shrink class to navbar */
    if ($(document).scrollTop() > 86) {
        $(".navbar").removeClass("not-shrink");
        $(".navbar").addClass("shrink");
    } else {
        $(".navbar").addClass("not-shrink");
        $(".navbar").removeClass("shrink");
    }

    /* Scrollspy Section */
    // Add scrollspy to <body>
    $('body').scrollspy({ target: ".navbar", offset: 300 });
    // Add smooth scrolling on all links inside the navbar
    $(".navbar-nav .nav-item .nav-link:not(.posts)").on('click', function(event) {
        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();
            event.stopPropagation();
            // Store hash
            var hash = this.hash;
            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (500) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 500, function() {

                // Add hash (#) to URL when done scrolling (default click behavior)
                //  window.location.hash = hash;
            });
        } // End if
        $('.navbar-collapse').collapse('hide');
    });
    /* Scrollspy Section closed */

    /* Table of Content */
    if ($("#dinamicMenu").length) { // if dynamic menu is available
        $(".col-lg-8 h2").addClass("toc-h2");
        $(".col-lg-8 h3").addClass("toc-h3");
        $("#dinamicMenu").dynamicContentMenu({
            theme: "none",
            'selectors': ".toc-h2, .toc-h3",
            extendPage: false
        });
    }
    /* Table of content closed */

    /* Recent Posts */
    if ($("#recent-posts").length) { // if this is blog page 
        $('#recent-posts').load("/posts/recent-posts.html", function() {
        });
    }
    /* Recent Posts closed */

});


$(document).on("scroll", function() {
    /* adding shrink class to navbar */
    if ($(document).scrollTop() > 86) {
        $(".navbar").removeClass("not-shrink");
        $(".navbar").addClass("shrink");
    } else {
        $(".navbar").addClass("not-shrink");
        $(".navbar").removeClass("shrink");
    }
});