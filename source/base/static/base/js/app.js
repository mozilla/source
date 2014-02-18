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

// add the mobile menu
var snapper = new Snap({
    element: document.getElementById('snap-content-wrapper'),
    disable: 'left',
    minPosition: -205
});
$('.toggle-navigation').on('click', function() {
    if (snapper.state().state == 'right') {
        snapper.close();
    } else {
        snapper.open('right');
    }
    return false;
})

// https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
