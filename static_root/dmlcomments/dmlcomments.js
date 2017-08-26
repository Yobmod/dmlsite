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

// Initially disable submit button until text present. How get text bog id in django form?
$(document).ready(function() {
$("button#commentsubmit").prop("disabled", true);
$("textarea#id_text").on("input", function() {
	$("span#comment_length").text(140 - $(this).val().length);
  	if ($(this).val().length > 0) {
    	$("button#commentsubmit").prop("disabled", false);
  	} else {
    	$("button#commentsubmit").prop("disabled", true);
  }
});
});
