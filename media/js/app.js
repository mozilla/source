$(document).ready(function () {
    var top = $('#main-logo').offset().top - parseFloat($('#main-logo').css('margin-top').replace(/auto/, 0));
    $(window).scroll(function (event) {
        // what the y position of the scroll is
        var y = $(this).scrollTop();
  
        // whether that's below the form
        if (y >= top) {
            // if so, add the fixed class
            $('.sourcelogomin').fadeIn(100);
        } else {
            // otherwise remove it
            $('.sourcelogomin').fadeOut(100);
        }
    });
});