function b(i,num,rate) {
    + new Date();
    var timeStamp = Date.now();
    var user = window.ip;
    var code = document.head.querySelector("[property~=in_code][content]").content;
    var sL = i[0];
    var eL = i[1];
    var bugList = ['blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy','unchecked_send_bug','unprotected_functions', 'withdraw_option', 'wrong_constructor_name'];
    // var bugList = ['Overflow_bug', 'blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy','unchecked_send_bug','unprotected_functions', 'withdraw_option', 'wrong_constructor_name'];
    var bugType = bugList[i[2]];
//     alert(timeStamp+" "+user+" "+code+" "+sL+" "+eL+" "+bugType+" "+rate);
    }
