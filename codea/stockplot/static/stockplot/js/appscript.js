//----------------------------------------------------------------------
//-----------Javascript for stockplot app-------------------------------
//----------------------------------------------------------------------


var names = [];

// main document ready function ----------------------------------------
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
            $target = $target.length && $target || $('[name=' + this.hash.slice(1) +']');
            if ($target.length) {
                var targetOffset = $target.offset().top - 50;
                $('html,body').animate({scrollTop: targetOffset}, 1000);
                return false;
            }
        }
    });

    
    // form that gets stock data:
    $('#stockform').submit(function(e){
        e.preventDefault();
        $('.div-plot').css('animation', 'plotlights 0.5s linear forwards');
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
// end of document ready funtion!---------------------------------------


//----------------------------------------------------------------------
//----------------------------------------------------------------------
//----------------------------------------------------------------------


// function for plotting stocks in d3.js--------------------------------
function plotStock(){
    $("#visualisation").empty();
    //lines = [];
    
    // calculate and set height for d3 plot. in #visualisation div:
    height = $(window).height() * 0.6;
    $(".plotbox").height(height);
    width = $(".plotbox").width();
    $("#visualisation").height(height);
    $("#visualisation").width(width);

    // variable for different colors:
    var color = d3.scale.category20();
    
    //------------------------------------------------------------------
    // get min max dates for x - axis-----------------------------------
    var xmin = gettimeframe();
    if (xmin === 'max'){
    xmin = d3.min(plotData, function(d) {
          return d3.min(d, function(e){
                return e.date;
                });
        });
    }
    var xmax = d3.max(plotData, function(d) {
      return d3.max(d, function(e){
          return e.date;
      });
    });
    
    //------------------------------------------------------------------
    // get min and max for y axis (beginning with lowest date on xaxis):
    ymin = d3.min(plotData, function(d) {
      return d3.min(d, function(e){
            if (e.date > xmin){
                return e.price;  
            } else {
                return Number.MAX_SAFE_INTEGER;
            }
      });
    })
    ymax = d3.max(plotData, function(d, i) {
      return d3.max(d, function(e){
            if (e.date > xmin){
                return e.price;
            } else {
                return 0;
            }
      });
    })
    
    //------------------------------------------------------------------
    // set variables for d3 plot----------------------------------------
    var margin = {
        top: 20,
        right: 20,
        bottom: 20,
        left: 50
    };
    width = width - margin.left - margin.right;
    height = height - margin.top - margin.bottom;

    // set variables for x and y ranges:
    var xRange = d3.time.scale().range([0, width]).domain([xmin, xmax]),
    yRange = d3.scale.linear().range([height, 0]).domain([ymin, ymax]);
    
    //------------------------------------------------------------------
    // variable for zoom------------------------------------------------
    var zoom = d3.behavior.zoom()
        .x(xRange)
        .y(yRange)
        .scaleExtent([0.1, Infinity])
        .on("zoom", zoomfun);

    //------------------------------------------------------------------
    // create svg and append stuff--------------------------------------
    svg = d3.select('#visualisation')
        .append("svg:svg")
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append("svg:g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(zoom);
    svg.append("svg:rect")
        .attr("width", width)
        .attr("height", height)
        .attr("fill-opacity", 0) // fill-opacity instead of fill none,
        // "fill" "none" hurts performance somehow...
        .attr("class", "plot");


    //------------------------------------------------------------------
    // functions for making x and y axes--------------------------------
    var make_x_axis = function () {
        return d3.svg.axis()
            .scale(xRange)
            .orient("bottom")
            .ticks(5); // ticks for grid - to be added
    };
    var make_y_axis = function () {
        return d3.svg.axis()
            .scale(yRange)
            .orient("left")
            .ticks(5);
    };


    //------------------------------------------------------------------
    // variables for x and y axes + append to svg-----------------------
    var xAxis = d3.svg.axis()
        .scale(xRange)
        .tickSize(1)
        .tickSubdivide(true) // maybe
        .orient("bottom")
        .ticks(5);

    svg.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, " + height + ")")
        .style("fill", "#F3EFE0")
        .call(xAxis);

    var yAxis = d3.svg.axis()
        .scale(yRange)
        .tickSize(1)
        .tickSubdivide(true)
        .orient("left")
        .ticks(5);

    svg.append("g")
        .attr("class", "y axis")
        .style("fill", "#F3EFE0")
        .call(yAxis);

    //------------------------------------------------------------------
    // Add x and y grid-------------------------------------------------
    svg.append("g")
        .attr("class", "x grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_axis()
        .tickSize(-height, 0, 0)
        .tickFormat(""));

    svg.append("g")
        .attr("class", "y grid")
        .call(make_y_axis()
        .tickSize(-width, 0, 0)
        .tickFormat(""));
    
    //------------------------------------------------------------------
    // append y-axis label----------------------------------------------
    svg.append("text")
      .attr("text-anchor", "end")
      .attr("y", -margin.left)
      .attr("x", -height/2)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .style("text-anchor", "middle")
      .style("fill", "#F3EFE0")
      .text("Stock price ($)");
    
    //------------------------------------------------------------------  
    // create tooltips-------------------------------------------------- 
    var tooldiv = d3.select("#plot-div").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
     var toolTipScale = d3.scale.linear().domain([height + 
        margin.top, margin.top]).range([ymin, ymax]);

    //------------------------------------------------------------------
    // append clipPath--------------------------------------------------
    svg.append("clipPath")
        .attr("id", "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);
    
    //------------------------------------------------------------------
    // create line------------------------------------------------------
    var line = d3.svg.line()
        .x(function (d) {
            return xRange(d.date);
        })
        .y(function (d) {
            return yRange(d.price);
        })
        .interpolate('linear');

    // append line:
    svg.selectAll('.line')
        .data(plotData)
        .enter()
        .append("path")
        .attr("id", "myPath")
        .attr("class", "line")
        .attr("clip-path", "url(#clip)")
        .attr('stroke', function(d,i){ 			
            return color(i);
        })
        .attr("d", line)
        .on("mousemove", function (d, i) { // add mousemove and mouseout
            //functions for tooltips
            var distanceDiv = $('#visualisation').offset().top;
            tooldiv.transition()
                .duration(100)
                .style("opacity", 0.9);
           tooldiv.html(Math.ceil(toolTipScale( d3.event.pageY-distanceDiv )) )
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");
		})
        .on("mouseout", function (d) {
            tooldiv.transition()
                .duration(1000)
                .style("opacity", 0);
            
        });


    //------------------------------------------------------------------    
    // append legend----------------------------------------------------
    var legendRectSize = 16;
    var legendSpacing = 4;
    var legend = svg.selectAll('.legend')
      .data(names)
      .enter()
      .append('g')
      .attr('class', 'legend')
      .attr('transform', function(d, i) { // set vertical and horizontal
        // offset of legen here
        var legendheight = legendRectSize + legendSpacing;
        var offset =  legendheight * i;
        var horz = 5;
        var vert = 2 + offset;
        return 'translate(' + horz + ',' + vert + ')';
      });
      
    legend.append('circle')
      .attr('r', legendRectSize/2)
      //.attr('height', legendRectSize)
      .attr('cx', legendRectSize/2)
      .attr('cy', (legendRectSize+legendSpacing)/2)
      .style('fill', function(d, i){
          return color(i);
          })
      .style('stroke', function(d, i){
          return color(i);
          })
      
    legend.append('text')
      .attr('x', legendRectSize + legendSpacing)
      .attr('dy', legendRectSize)
      .style("fill", "#F3EFE0")
      .text(function(d,i){
            return names[i];
          });

    //------------------------------------------------------------------
    // function for zoom------------------------------------------------
    function zoomfun() {
        // reset scales when zoom out of bounds:
        var resetScale = 0;
          if ((xRange.domain()[1] - xRange.domain()[0]) >= (xmax - xmin)) {
            zoom.x(xRange.domain([xmin, xmax]));
            resetScale = 1;
          }
          if ((yRange.domain()[1] - yRange.domain()[0]) >= (ymax - ymin)) {
            zoom.y(yRange.domain([ymin, ymax]));
            resetScale += 1;
          }
          if (resetScale == 2) { // Both axes are out of bounds. Reset.
            zoom.scale(1); // zoom to 1
          }
          else {
            // different cases if out of bounds in one direction:
            if (xRange.domain()[1] > xmax){
                // important!!! date substraction here:
                var xminnew = new Date(xRange.domain()[0].getTime() - 
                    xRange.domain()[1].getTime() + xmax.getTime());
                xRange.domain([xminnew, xmax]);
            }
            if (xRange.domain()[0] < xmin){
                var xmaxnew = new Date(xRange.domain()[1].getTime() - 
                    xRange.domain()[0].getTime() + xmin.getTime());
                xRange.domain([xmin, xmaxnew]);
            }
            if (yRange.domain()[1] > ymax){
                var yminnew = yRange.domain()[0] - yRange.domain()[1] + ymax;
                yRange.domain([yminnew, ymax]);
            }
            if (yRange.domain()[0] < ymin){
                var ymaxnew = yRange.domain()[1] - yRange.domain()[0] + ymin;
                yRange.domain([ymin, ymaxnew]);
            }
          }
        
        //change toolTipScale to new domain:
        toolTipScale = d3.scale.linear().domain([height + margin.top, 
            margin.top]).range([yRange.domain()[0], yRange.domain()[1]]);
        svg.select(".x.axis").call(xAxis);
        svg.select(".y.axis").call(yAxis);
        svg.select(".x.grid")
            .call(make_x_axis()
            .tickSize(-height, 0, 0)
            .tickFormat(""));
        svg.select(".y.grid")
            .call(make_y_axis()
            .tickSize(-width, 0, 0)
            .tickFormat(""));
        svg.selectAll('path.line').attr('d', line);

    }
}


//----------------------------------------------------------------------
//----------------------------------------------------------------------
//----------------------------------------------------------------------


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


//----------------------------------------------------------------------
//----------------------------------------------------------------------
//----------------------------------------------------------------------


// Generates button with different methods for stocks.
// For now: only moving average!
function createStockMethods(stocksymbol){
    
    //stockclass because . can lead to errors in JQuery!
    var stockclass = stocksymbol.replace('.', '-');
    var html = '<div class = "btn-group div-' + stockclass + '">';
    html += '<button type ="button" class="btn btn-default dropdown-toggle btn-sm btn-stock" data-toggle ="dropdown" aria-haspopup ="true" aria-expanded="false">';
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


//----------------------------------------------------------------------
//----------------------------------------------------------------------
//----------------------------------------------------------------------



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
                case '10y':
                    fromtime = d3.time.year.offset(curtime, -10);
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

