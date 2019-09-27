$(document).ready(function(){
    $(".navbar-toggler").click(function(){
        $(".menu").toggleClass("active");
    })

    $(document).ready(function(){       
        var scroll_start = 0;
        var startchange = $('#startchange');
        var offset = startchange.offset();
        var navbar = $(".navbar");
        var navHeight = navbar.height();
        var stickyFlag = true;
        var unStickyFlag = false;
        if (startchange.length){
            $(document).scroll(function(){ 
                scroll_start = $(this).scrollTop();
                if (scroll_start > offset.top && stickyFlag){
                    stickyFlag = false;
                    unStickyFlag = false;
                    navbar.addClass("fixed-top")
                          .css({
                              "padding": "4vw 2.5vw", 
                              "top": "-=170px"
                          })
                          .animate({top: "0px"}, 500)
                } else if (scroll_start <= offset.top){
                    if (!unStickyFlag && !stickyFlag){
                        console.log("bla")
                        stickyFlag = true;
                        unStickyFlag = true;
                        navbar.animate({top: "-170px"}, function(){
                            navbar.removeClass("fixed-top")
                                  .css("top", "0px")
                        });
                    }
                }
            });
         }
     });
})

