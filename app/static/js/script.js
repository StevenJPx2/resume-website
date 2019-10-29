$(document).ready(function(){

    var navTogg = $(".navbar-toggler");
    var menu = $(".menu");
    var footer = $("footer");
    var clickFlag = false;

    navTogg.click(function(){
        if (!clickFlag){
            menu.toggleClass("active");
        }
    })
    
    $(".container-fluid").click(function(){
        if ($(window).width() <= 1200){
            if (menu.hasClass("active")){
                menu.removeClass("active");
                clickFlag = true;
                navTogg.trigger("click");
                clickFlag = false;
            }
        }
    })

    if ($("body").height() < $(window).height()-40 && $(window).width() >= 768) {
        footer.css("bottom", "0")
    }
})