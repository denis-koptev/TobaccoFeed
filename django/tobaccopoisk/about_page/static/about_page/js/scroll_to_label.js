 $(document).ready(function(){
    $("#sections").on("click","a", function (event) {
        event.preventDefault();
        if ($(this).attr('href').indexOf('#') >= 0) {
	        var id  = $(this).attr('href'),
	            top = $(id).offset().top;
	        $('body,html').animate({scrollTop: top}, 800);
        } else {
        	location.href = $(this).attr('href');
    	}
    });
});