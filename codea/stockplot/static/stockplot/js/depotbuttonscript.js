//----------------------------------------------------------------------
//-----------Javascript for button in depot column ---------------------
//----------------------------------------------------------------------

// main document ready function ----------------------------------------
$(document).ready(function(){

    /*
    // button used for selling stock:
    $('.btn-sell').on('click touchstart', function (e) {
        e.stopPropagation();
        var stock;
        stock = $(this).attr("stock")
        $.get('./', {stock: stock}, function(json){
            //plotData = json['plotData'];
            //names = json['names']
            //plotStock();
            console.log(json['text']);
        });
	});*/

    // form that gets stock data:
    $('.sellform').submit(function(e){
        e.preventDefault();
        e.stopPropagation();
        var stock = $(this).attr("stock");
        $.ajax({
               url : './',
               type : "POST",
               // send data to django view:'
               data: $(this).serialize() + '&stock=' + stock,
               // successfull return of json data from django view:
               success : function(json) {
                   // get data from jsoN:
                   console.log(json['text']);
                   },
        });
    });
});



// end of document ready funtion!---------------------------------------
