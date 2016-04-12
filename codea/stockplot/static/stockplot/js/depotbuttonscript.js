//----------------------------------------------------------------------
//-----------Javascript for button in depot column ---------------------
//----------------------------------------------------------------------

// main document ready function ----------------------------------------
$(document).ready(function(){

    // button used for selling stock:
    $('.btn-sell').on('click touchstart', function (e) {
        e.stopPropagation();
        var stock;
        stock = $(this).attr("stock")
        $.get('./', {stock: stock}, function(json){
            /*plotData = json['plotData'];
            names = json['names']
            plotStock();*/
            console.log(json['text']);
        });
	});
});
// end of document ready funtion!---------------------------------------
