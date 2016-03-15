//----------------------------------------------------------------------
//-----------Javascript for registration--------------------------------
//----------------------------------------------------------------------

// main document ready function ----------------------------------------
$(document).ready(function(){


    // form that gets stock data:
    $('#formregister').submit(function(e){
        e.preventDefault();
        //$.post('./', $(this).serialize());
        $.ajax({
            url: './',
            type: "POST",
            data: $(this).serialize(),

            success: function(json){
                error_message = json['error_message'];
                message = json['message'];
                if (error_message !== ''){
                    $('#message').addClass('jumbotron');
                    $('#message').addClass('errortext');
                    $('#message').append(error_message);
                } else if (message !== ''){
                    $('#message').addClass('jumbotron');
                    $('#message').addClass('messagetext');
                    $('#message').append(message);
                }
            },
        });
    });


});
// end of document ready funtion!---------------------------------------
