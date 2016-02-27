$(document).ready(function(){
	setNavbar();
	
	$('#nav-button').on('click touchstart', function () {
		
		if($('.navbar-collapse').hasClass('in')){
			$('#span-top').css('animation', 'rotate2 0.2s ease-in forwards');
			$('#span-bottom').css('animation', 'rotateBack2 0.2s ease-in forwards');
			$('#span-top').removeClass('span-top-rotated');
			$('#span-bottom').removeClass('span-bottom-rotated');
		} else {
			$('#span-top').addClass('span-top-rotated');
			$('#span-bottom').addClass('span-bottom-rotated');
			$('#span-top').css('animation', 'rotate 0.2s ease-in forwards');
			$('#span-bottom').css('animation', 'rotateBack 0.2s ease-in forwards');
		}
	});
	
	$(window).resize(function(){
		setNavbar();
	});
	
	window.addEventListener( "scroll", function( event ) {
		setNavbar();
	});	
	
	
	$('a[href*=#]').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
    && location.hostname == this.hostname) {
      var $target = $(this.hash);
      $target = $target.length && $target
      || $('[name=' + this.hash.slice(1) +']');
      if ($target.length) {
        var targetOffset = $target.offset().top - 50;
        $('html,body')
        .animate({scrollTop: targetOffset}, 1000);
       return false;
		  }
		}
	  });
	
	function setNavbar(){
	
		var distanceBar = $('#navbar').offset().top;
		var distanceContact = $('#contact').offset().top;
		var windowScroll = $(window).scrollTop();

		if(windowScroll + 60 > distanceContact){
			$('.navbar-pos').css('position', 'fixed');
			$('.navbar-pos').css('top', '0');
			$('#contactlink').addClass('link-active');
			$('#homelink').removeClass('link-active');
			$('#aboutlink').removeClass('link-active');
		} else if (windowScroll > distanceBar){
			$('.navbar-pos').css('position', 'fixed');
			$('.navbar-pos').css('top', '0');
			$('#aboutlink').addClass('link-active');
			$('#homelink').removeClass('link-active');
			$('#contactlink').removeClass('link-active');
		} else if (windowScroll + 10 > distanceBar){
			$('.navbar-pos').css('position', 'absolute');
			$('.navbar-pos').css('top', '0');
			$('#aboutlink').addClass('link-active');
			$('#homelink').removeClass('link-active');
			$('#contactlink').removeClass('link-active');
		} else {
			$('.navbar-pos').css('position', 'absolute');
			$('.navbar-pos').css('top', '');
			$('#homelink').addClass('link-active');
			$('#aboutlink').removeClass('link-active');
			$('#contactlink').removeClass('link-active');
		}
	};
});
