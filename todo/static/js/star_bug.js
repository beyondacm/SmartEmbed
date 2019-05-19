function b(i,num,rate) {
    + new Date();
    var timeStamp = Date.now();
    var user = window.ip;
    var code = document.head.querySelector("[property~=in_code][content]").content;
    var sL = i[0];
    var eL = i[1];
    // var bugList = ['blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy','unchecked_send_bug','unprotected_functions','withdraw_option','wrong_constructor_name'];
    var bugList = ['Overflow_bug', 'Honeypot_bug', 'OwnerCVE_bug', 'PRNG_bug', 'blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy']
    var bugType = bugList[i[2]];
    
    jQuery.ajax({
        url: '/dbhandle_bug?user='+user+'&code='+code+'&sl='+sL+'&el='+eL+'&bugtype='+bugType+'&rate='+rate,
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
