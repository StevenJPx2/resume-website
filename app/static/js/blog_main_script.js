$(document).ready(function () {
  
    'use strict';
    
     var c, currentScrollTop = 0,
         navbar = $('.navbar'),
         logo = $("#blog-logo-main"),
         smallLogo = $('#blog-logo'),
         leftLink = $("#left-link"),
         rightLink = $("#right-link"),
         stickyFlag = true,
         unStickyFlag = false;


     $(window).scroll(function () {
        var a = $(window).scrollTop();
        var b = navbar.height();
       
        currentScrollTop = a;
       
        if (c < currentScrollTop && a > b + b && stickyFlag) {
            stickyFlag = false;
            unStickyFlag = false;
            if ($(window).width() >= 768) {
                logo.animate({
                    top: "-130px",
                    opacity: 0
                })
                navbar.animate({height: "103px"}, 600)
                leftLink.animate({left: "223px"}, 600)
                rightLink.animate({left: "-223px"}, 600)
            } else {
                // smallLogo.animate({height: "2rem"})
            }
            
        } else if (c > currentScrollTop && !(a <= b) && (!unStickyFlag && !stickyFlag)) {
            stickyFlag = true;
            unStickyFlag = true;
            if ($(window).width() >= 768) {
                logo.animate({
                    top: "0px",
                    opacity: 1
                })
                navbar.animate({height: "200px"}, 300)
                leftLink.animate({left: "0px"}, 300)
                rightLink.animate({left: "0px"}, 300)
            } else {
                // smallLogo.animate({height: "2rem"})
            }
        }
        c = currentScrollTop;
    });
  });