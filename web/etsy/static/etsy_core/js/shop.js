var currentFs, nextFs, previousFs; //fieldsets
var left, opacity, scale; //fieldset properties wich will be animate

$("#goToThePreferences").click(function() {
	currentFs = $("#nameFs");
	preferencesFs = $("#preferencesFieldset");
	preferencesFs.show();
	currentFs.hide();
})

$("#goToName").click(function() {
	currentFs = $("#preferencesFieldset");
	preferencesFs = $("#nameFs");
	preferencesFs.show();
	currentFs.hide();
})

$("#goToNameButton").click(function() {
	currentFs = $("#preferencesFieldset");
	preferencesFs = $("#nameFs");
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(currentFs)).removeClass("active");
    $("#progressbar li").eq($("fieldset").index(preferencesFs)).addClass("active");
	
	currentFs.hide();
	preferencesFs.show();
})