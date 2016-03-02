$(document).ready(function(){
	setNavbar();
    plotStock();
	
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
        $("#visualisation").empty();
        plotStock();
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


    $('#stockform').submit(function(e){
        //$.post('/stockplot/', $(this).serialize(), function(data){
        //   $('#stocksymbol').val();
        //});
        e.preventDefault();
        //Prepare csrf token
        var csrftoken = getCookie('csrftoken');
        var stocksymbol = $('#stocksymbol').val();
        $.ajax({
               url : '/stockplot/',
               type : "POST", 
               data : { csrfmiddlewaretoken : csrftoken, 
               stocksymbol : stocksymbol,
               },
        success : function(json) {
               // append plotData here
               stockData = json['stockData'];
               for(var i = 0; i < stockData.length; i++){
                   stockData[i].date = new Date(stockData[i].date);
               }
               plotData.push(stockData);
               plotStock();
               },  
        });
    });

    $('#clear').on('click touchstart', function () {
        plotData = [];
        plotStock();
	});

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

function plotStock(){
    $("#visualisation").empty();
    
    height = $(window).height() * 0.5;
    $(".plotbox").height(height);
    width = $(".plotbox").width();
    
    $("#visualisation").height(height);
    $("#visualisation").width(width);
    
    console.log(plotData);

    var color = d3.scale.category20();
     
    var vis = d3.select('#visualisation'),
        WIDTH = width,
        HEIGHT = height,
        MARGINS = {
          top: 20,
          right: 20,
          bottom: 20,
          left: 50
        },
        xRange = d3.time.scale().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(plotData, function(d) {
          return d3.min(d, function(e){
                return e.date;
          });
        }), d3.max(plotData, function(d) {
          return d3.max(d, function(e){
              return e.date;
          });
        })]),
        yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(plotData, function(d) {
          return d3.min(d, function(e){
            return e.price;  
          });
        }), d3.max(plotData, function(d, i) {
          return d3.max(d, function(e){
                return e.price;
          });
        })]),
        xAxis = d3.svg.axis()
          .scale(xRange)
          .tickSize(1)
          .tickSubdivide(true)
          .orient("bottom"),
        yAxis = d3.svg.axis()
          .scale(yRange)
          .tickSize(1)
          .orient('left')
          .tickSubdivide(true);
    

    vis.append('svg:g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
      .call(xAxis);

    vis.append('svg:g')
      .attr('class', 'y axis')
      .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
      .call(yAxis);

    // append y-axis label
    vis.append("text")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("x", -(height-MARGINS.left)/2)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .style("text-anchor", "middle")
      .text("Stock price ($)");


    var lineFunc = d3.svg.line()
      .x(function(d) {
        return xRange(d.date);
      })
      .y(function(d) {
        return yRange(d.price);
      })
      .interpolate('linear');
    
    
    if (plotData !== undefined && plotData.length !== 0){
        for(var i = 0; i < plotData.length; i++){
            vis.append('svg:path')
              .attr('d', lineFunc(plotData[i]))
              .attr('stroke', color(i));
        }
    }
}

//For getting CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
