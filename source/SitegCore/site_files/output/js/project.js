const $nav = $(".nav-slides .gallery");
const $main = $(".main-slides .gallery");
const isMore = $('.nav-slides .sizer').length>4?true:false;

if (isMore) {
    $('#gallery .nav-slides').show();
} else {
    $('#gallery .nav-slides').hide();
}

$main.slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    dots: false,
    autoplay: true,
    asNavFor: '.nav-slides .gallery',
    responsive: [{
        breakpoint: 480,
        settings: {
            dots: true
        }
    }]
});

$nav.slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    asNavFor: '.main-slides .gallery',
    prevArrow: ".arrow-left",
    nextArrow: ".arrow-right",
    dots: true,
    centerMode: true,
    focusOnSelect: true,
    responsive: [{
            breakpoint: 768,
            settings: {
                slidesToShow: 2
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 1
            }
        },
    ]
});