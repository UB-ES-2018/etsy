var currentFs, nextFs, previousFs; //fieldsets
var left, opacity, scale; //fieldset properties wich will be animate
var animating; 

$(".next").click(function(){
    if (animating) 
        return false;
    
    animating = true;
    currentFs = $(this).parent;
    nextFs = $(this).parent().next();

    $("#progressbar li").eq($("fieldset").index(nextFs)).addClass("active");

    nextFs.show();

    currentFs.animate({
        opacity:0
        }, 
        {step: function(now, mx) {
            sacle = 1 - (1 - now) *  0.2;
            left = (now * 50) + "%";
            opacity = 1 - now;

            currentFs.css({
                'transform': 'scale('+scale+')',
                'position': 'absolute'
            });

            nextFs.css({
                'left': left,
                'opacity': opacity
            });
        },

        duration: 800,
        complete: function(){
            currentFs.hide();
            animating = false;
        },
        easing: 'easeInOutBack'
    });
});

