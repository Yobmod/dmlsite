$(document).ready(function() {
    $('[data-toggle=tooltip]').tooltip();
});

$(document).ready(function() {
	var randNum = Math.floor(Math.random() * 10);
	if(randNum < 1){
		$(".randomfade").fadeTo("slow", 1.00);
		$(".randomfade").fadeTo("slow", 0.00);
	} else{};
});

$(document).ready(function() {
	$("#fadeimg").click(function(){
		$("#fadeimg").fadeTo(5000, 0.05);
});
});
