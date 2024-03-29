$(document).ready(function(){
    
    var scroll_start = 0;
    var startchange = $('#startchange');
    var offset = startchange.offset();
    var navbar = $(".navbar");
    var stickyFlag = true;
    var unStickyFlag = false;
    
    if (startchange.length){
        $(document).scroll(function(){ 
            scroll_start = $(this).scrollTop();
            if (scroll_start > offset.top && stickyFlag){
                stickyFlag = false;
                unStickyFlag = false;
                navbar.addClass("fixed-top")
                        .removeClass("pad-navbar")
                        .css({
                            "padding": "2.5rem 4.5rem", 
                            "top": "-=170px"
                        })
                        .animate({top: "0px"}, 500)
            } else if (scroll_start <= offset.top){
                if (!unStickyFlag && !stickyFlag){
                    stickyFlag = true;
                    unStickyFlag = true;
                    navbar.animate({top: "-170px"}, function(){
                        navbar.removeClass("fixed-top")
                                .addClass("pad-navbar")
                                .css("top", "0px")
                    });
                }
            }
        });
        }

})

