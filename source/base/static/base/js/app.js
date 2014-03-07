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

var gaTrackEvent = function(category, action, label) {
    // make sure we have Google Analytics function available
    if (typeof(ga) == 'function') {
        ga('send', 'event', category, action, label);
    }
}

// http://www.hnldesign.nl/work/code/debouncing-events-with-jquery/
var jQueryDebounce = function($,cf,of, interval) {
    // deBouncer by hnldesign.nl
    // based on code by Paul Irish and the original debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
        var timeout;

        return function debounced () {
            var obj = this, args = arguments;
            function delayed () {
                if (!execAsap)
                    func.apply(obj, args);
                timeout = null;
                }
                if (timeout)
                    clearTimeout(timeout);
                else if (execAsap)
                    func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || interval);
        };
    };
    jQuery.fn[cf] = function(fn){ return fn ? this.bind(of, debounce(fn)) : this.trigger(cf); };
};

// debounce the resize event, and apply nav pane if necessary
jQueryDebounce(jQuery,'smartresize', 'resize', 100);
$(window).smartresize(function(e) {
    applyNavPane();
})

// snap.js nav pane
var navPane = new Snap({
    element: document.getElementById('snap-content-wrapper'),
    disable: 'left',
    slideIntent: 30,
    minDragDistance: 20,
    minPosition: -205
});
$('.toggle-navigation').on('click', function() {
    if (navPane.state().state == 'right') {
        navPane.close();
    } else {
        navPane.open('right');
    }
    return false;
})

// only enable the snap.js nav pane if appropriate for browser width
var applyNavPane = function() {
    window.browserWidth = document.documentElement.clientWidth;

    if (browserWidth <= 480) {
        navPane.enable();
        $('.snap-drawers').removeClass('hidden')
    } else {
        navPane.disable();
        $('.snap-drawers').addClass('hidden')
    }
}
// initial page load
applyNavPane();

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
