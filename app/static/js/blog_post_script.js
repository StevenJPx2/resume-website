$(document).ready(function () {
  
    'use strict';
    
    var c = 20,
        navbar = $(".navbar"),
        navBack = $('#nav-back'),
        smallLogo = $("#blog-logo"),
        logo = $("#blog-logo-main"),
        leftLink = $("#left-link"),
        rightLink = $("#right-link"),
        backIcon = $('#back'),
        stickyFlag = true,
        unStickyFlag = false;

    $(window).scroll(function () {
        var a = $(window).scrollTop();
                
        if (c < a && stickyFlag) {
            stickyFlag = false;
            unStickyFlag = false;
            if ($(window).width() >= 768) {
                logo.animate({
                    top: "-130px",
                    opacity: 0
                })
                navbar.animate({height: "103px"}, 600)
                navBack.animate({
                    height: "103px",
                    opacity: 1
                }, 600)
                leftLink.animate({left: "203px"}, 600)
                rightLink.animate({left: "-203px"}, 600)
                backIcon.animate({top: "1px"}, 600)
            } else {
                console.log("")
                navBack.animate({opacity: 1})
            }
            
        } else if (c >= a && (!unStickyFlag && !stickyFlag)) {
            stickyFlag = true;
            unStickyFlag = true;
            if ($(window).width() >= 768) {
                logo.animate({
                    top: "0px",
                    opacity: 1
                })
                navbar.animate({height: "200px"}, 300)
                navBack.animate({
                    height: "200px",
                    opacity: 0.46
                }, 300)
                leftLink.animate({left: "0px"}, 300)
                rightLink.animate({left: "0px"}, 300)
                backIcon.animate({top: "-130px"}, 300)
            } else {
                console.log("")
                navBack.animate({opacity: 0.46})
            }
    }
    });
  });