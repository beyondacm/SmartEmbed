function c(clone,sim,num,rate) {
    + new Date();
    var timeStamp = Date.now();
    var user = window.ip;
    var code = document.head.querySelector("[property~=in_code][content]").content;

    jQuery.ajax({
        url: '/dbhandle_clone?user='+user+'&code='+code+'&clone='+clone+'&sim='+sim+'&rate='+rate,
        type: 'GET',
        error: function(xhr, status, error) {
//             alert(xhr.responseText);
            var a = 0;
        },
        success: function(results) { 
            var a = 1;
        }
    });
    }
