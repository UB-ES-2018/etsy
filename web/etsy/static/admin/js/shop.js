var currentFs, nextFs, previousFs; //fieldsets
var left, opacity, scale; //fieldset properties wich will be animate
var animating; 

$(".next").click(function(){
    
    currentFs = $(this).parent();
    
    nextFs = currentFs.next();

    $("#progressbar li").eq($("fieldset").index(nextFs)).addClass("active");

    nextFs.show();
    currentFs.hide();
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	
});

$("#goToThePreferences").click(function() {
	
})