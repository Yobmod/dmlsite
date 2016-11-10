$(document).ready(function() {
    $('.fade000').mouseenter(function() {//when moused over
        $('.fade000').fadeTo('fast', 0.00); //speed, opacity as decimal
    });
});


$(document).ready(function() {
   $(".slidedown").slidedown("slow");	//speed of slide
});

$(document).ready(function() {
    $('div').mouseenter(function() {//when moused over
        $('div').hide();//hides
    });
});