var button = jQuery('.button');
var preloader = jQuery('#preloader');
var longitudediv = jQuery('.longitude');
var lattitudediv = jQuery('.lattitude');
var locationdiv = jQuery('.location');

if (navigator.geolocation) {    
    // Browser supports it, we're good to go!     
    } else {    
    alert('Sorry your browser doesn\'t support the Geolocation API');    
    }

    button.click(function(e) {
        e.preventDefault();
        preloader.show();
        navigator.geolocation.getCurrentPosition(exportPosition, errorPosition);
    });

