var names = [];

$(document).ready(function(){
    plotStock(); // when doc ready, plot
	
    // collapsed navbar
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
	
    // on window resize replot:
	$(window).resize(function(){
        $("#visualisation").empty();
        plotStock();
	});
	
	// animation for smooth scroll:
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

    
    // from that gets stock data:
    $('#stockform').submit(function(e){
        e.preventDefault();
        var csrftoken = getCookie('csrftoken'); //Prepare csrf token
        var stocksymbol = $('#stocksymbol').val();
        var method = 'plot';
        $.ajax({
               url : '/stockplot/stockapp/',
               type : "POST", 
               // send data to django view:
               data : { csrfmiddlewaretoken : csrftoken, 
                        stocksymbol : stocksymbol,
                        method : method,
               },
        // successfull return of json data from django view:
        success : function(json) {
               // append plotData here
               stockData = json['stockData'];
               for(var i = 0; i < stockData.length; i++){
                   stockData[i].date = new Date(stockData[i].date);
               }
               // create button with methods:
               createStockMethods(stocksymbol);
               // add to plotData and names and then plot:
               plotData.push(stockData);
               names.push(stocksymbol); 
               plotStock();
               },  
        });
    });
 
    // clear plots:
    $('#clear').on('click touchstart', function () {
        names = [];
        plotData = [];
        $('#box-top').html("");
        plotStock();
	});
    
    
    // button group with .btn-timeframe's sets timeframe for plot:
    $('.btn-timeframe').on('click touchstart', function(e){
        var timeframe = e.target.id;
        $('.btn-timeframe').removeClass('active');
        $('#'+timeframe).addClass('active');        
        plotStock();
    });

});


// functionf or plotting stocks in d3.js:
function plotStock(){
    $("#visualisation").empty();
    
    height = $(window).height() * 0.6;
    $(".plotbox").height(height);
    width = $(".plotbox").width();
    
    $("#visualisation").height(height);
    $("#visualisation").width(width);

    var color = d3.scale.category20();
    
    var fromtime = gettimeframe();
    
    if (fromtime === 'max'){
        fromtime = d3.min(plotData, function(d) {
                                      return d3.min(d, function(e){
                                            return e.date;
                                      });
                        });
    }
     
    var vis = d3.select('#visualisation'),
        WIDTH = width,
        HEIGHT = height,
        MARGINS = {
          top: 20,
          right: 20,
          bottom: 20,
          left: 50
        },
        xRange = d3.time.scale().range([MARGINS.left, WIDTH - MARGINS.right]).domain([fromtime, d3.max(plotData, function(d) {
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
    
    
    // append axes ticks:
    function make_x_axis() {        
        return d3.svg.axis()
            .scale(xRange)
            .orient("bottom")
            .ticks(4)
    }

    function make_y_axis() {        
        return d3.svg.axis()
            .scale(yRange)
            .orient("left")
            .ticks(4)
    }
    
    vis.append("svg:g")         
        .attr("class", "grid")
        .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
        .call(make_x_axis()
            .tickSize(-HEIGHT + MARGINS.top + MARGINS.bottom, 0, 0)
            .tickFormat("")
        )

    vis.append("svg:g")         
        .attr("class", "grid")
        .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
        .call(make_y_axis()
            .tickSize(-WIDTH + MARGINS.right + MARGINS.left, 0, 0)
            .tickFormat("")
        )
    

    // append axes:
    vis.append('svg:g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
      .style("fill", "#F3EFE0")
      .call(xAxis);


    vis.append('svg:g')
      .attr('class', 'y axis')
      .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
      .style("fill", "#F3EFE0")
      .call(yAxis);

    // append y-axis label
    vis.append("text")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("x", -(HEIGHT-MARGINS.left)/2)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .style("text-anchor", "middle")
      .style("fill", "#F3EFE0")
      .text("Stock price ($)");


    // append clip to cut off anything outside of xRange:
    
    var clip = vis.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("id", "clip-rect")
        .attr("x", MARGINS.left)
        .attr("y", MARGINS.top)
        .attr("width", WIDTH)
        .attr("height", HEIGHT);

    // Plot data here:
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
              .attr('stroke', color(i))
              .attr("clip-path", "url(#clip)");
        }
    }

    
    // append legend:
    var legendRectSize = 18;
    var legendSpacing = 4;
    var legend = vis.selectAll('.legend')
      .data(names)
      .enter()
      .append('g')
      .attr('class', 'legend')
      .attr('transform', function(d, i) {
        var legendheight = legendRectSize + legendSpacing;
        var offset =  legendheight * i;
        var horz = MARGINS.left + 10;
        var vert = MARGINS.top + offset;
        return 'translate(' + horz + ',' + vert + ')';
      });
      
    legend.append('rect')
      .attr('width', legendRectSize)
      .attr('height', legendRectSize)
      .style('fill', function(d, i){
          return color(i);
          })
      .style('stroke', function(d, i){
          return color(i);
          })
      
    legend.append('text')
      .attr('x', legendRectSize + legendSpacing)
      .attr('y', legendRectSize - legendSpacing)
      .style("fill", "#F3EFE0")
      .text(function(d,i){
            return names[i];
          });
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


// Generates button with different methods for stocks.
// For now: only moving average!
function createStockMethods(stocksymbol){
    
    //stockclass because . can lead to errors in JQuery!
    var stockclass = stocksymbol.replace('.', '-');
    var html = '<div class = "btn-group div-' + stockclass + '">';
    html += '<button type ="button" class="btn btn-default dropdown-toggle btn-sm" data-toggle ="dropdown" aria-haspopup ="true" aria-expanded="false">';
    html += stocksymbol + '<span> + </span>';
    html += '</button>';
    html += '<ul class = "dropdown-menu">';
    html += '<li> <input type ="text" class ="form-control" placeholder = "Days" id = "' + stockclass + 'Days">';
    html += '<a href class = "' + stockclass + '_methods" id="' + stockclass + '_mvgAvg"> - Days - Moving Average </a></li>';
    html += '<li><a href class = "' + stockclass + '_methods" id="' + stockclass + '_expmvgAvg"> - Days - Exp. Moving Average </a></li>';
    html += '<li role="separator" class="divider"></li>'
    html += '<li><a href class = "delete" id ="' + stockclass + '_delete">Delete</a></li>';
    html += '</ul></div>';
    $('#box-top').append(html);
    
    // add event listener for moving average:
    $('.'+stockclass+'_methods').on('click touchstart', function(e){
        e.preventDefault();
        
        var csrftoken = getCookie('csrftoken'); //Prepare csrf token
        
        var stockstring = e.target.id.split('_');
        var stockclass = stockstring[0]; //get stockclass without .
        var stocksymbol = stockclass.replace('-', '.'); //replace to get actual stocksymbol
        var method = stockstring[1];
        var days = $('#'+stockclass+'Days').val();
        $.ajax({
               url : '/stockplot/stockapp/',
               type : "POST", 
               // data to send to django view
               data : { csrfmiddlewaretoken : csrftoken, 
                        stocksymbol : stocksymbol,
                        method: method,
                        days: days,
               },
        // in case of success do following with return json data:
        success : function(json) {
               // append plotData here
               stockData = json['stockData'];
               for(var i = 0; i < stockData.length; i++){
                   stockData[i].date = new Date(stockData[i].date);
               }
               plotData.push(stockData);
               names.push(stocksymbol + ' ' + days + ' days '+  method); 
               plotStock();
               },  
        });
    });
    
    // delete method for stock: deletes all plots with the selected
    // stocksymbol
    $('.delete').on('click touchstart', function(e){
        e.preventDefault();
        var stockstring = e.target.id.split('_');
        // take care: stockclass and stocksymbol different because of
        // JQuery errors with '.'
        var stockclass = stockstring[0];
        var stocksymbol = stockclass.replace('-', '.');
        // delete all names and plotData with stocksymbol:
        for (var i = names.length - 1; i >= 0; i--){
            if(names[i].indexOf(stocksymbol) > -1){
                names.splice(i, 1);
                plotData.splice(i, 1);
            }
        }
        // remove button div:
        $(".div-"+stockclass).remove();
        plotStock();
    });
}

// get timeframe for plot. Depends on button group btn-timeframe:
function gettimeframe(){
    var fromtime;
    $(".btn-timeframe").each(function(){
        if($(this).hasClass('active')){
            timeid = this.id;
            curtime = new Date();
            //curtime = d3.time.format("%Y-%m-%d").parse;
            switch(timeid){
                case '1d':
                    fromtime = d3.time.day.offset(curtime, -1);
                    break;
                case '1w':
                    fromtime = d3.time.day.offset(curtime, -7);
                    break;
                case '1m':
                    fromtime = d3.time.month.offset(curtime, -1);
                    break;
                case '1y':
                    fromtime = d3.time.year.offset(curtime, -1);
                    break;
                case '2y':
                    fromtime = d3.time.year.offset(curtime, -2);
                    break;
                case '5y':
                    fromtime = d3.time.year.offset(curtime, -5);
                    break;
                case 'max':
                    fromtime = 'max';
                    break;
                default:  
                    fromtime = 'max';
            }
        }
    })
    return fromtime;
}
