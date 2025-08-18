$(document).ready(function () {
//MAKING THE NAVINAGTION SLIDE IN AND OUT ON CLICK
    const navbar = $('#navbar_menu');
    const nav_btn_open = $('#nav_open').click(function (e) {
        e.preventDefault();
        $(this).fadeOut(100).fadeIn(100);
        navbar.css('left', '0');
    })
    const nav_bnt_close = $('#nav_close').click(function (e) {
        e.preventDefault();
        $(this).fadeOut(100).fadeIn(100);
        navbar.css('left', '-101%');
    })


    // Get current page URL path (without domain)
    let currentPath = window.location.pathname;

    $(".list-link").each(function() {
        let linkPath = $(this).attr("href");

        // Check if link matches current path
        if (linkPath === currentPath) {
            $(this).attr('id', 'active')
        }
    });



    //opening and closing nav menu
    //OPENING AND CLOSING OF NAVBAR DROPDOWNS
    $('.drop_down_arrow').click(function() {
        $('#drop_menu').fadeToggle(200); // Smooth transition
    });
});



//contrling how google icons appear when page loaded
$(window).on("load", function() {
    $(".material-symbols-outlined").css({'width': 'auto', 'opacity': '1'});
});



