$(document).ready(function() {
	$("#commentShowButton").click(function(){
		$("#commentShow").toggle(1000);
		});
});

$(document).ready(function() {
	$(".replyShowButton").click(function(event){
		event.preventDefault()
		$(this).parent().next(".replyShow").toggle(500);
	});
});

$(document).ready(function() {
	$(".addReplyShowButton").click(function(event){
		event.preventDefault()
		$(this).parent().next(".addReplyShow").toggle(1000);
	});
});
