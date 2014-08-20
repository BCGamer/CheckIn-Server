$(function(){



});


function checkVerification(){

    $.ajax({
        url: '/verify/check/',
        type: 'GET',
        success: function(data){
            console.log(data);
        }
    });

}


setInterval(checkVerification, 1000);