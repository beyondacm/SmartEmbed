// $(document).ready(function(){
//     // Check Radio-box
//     // $(".rating_1 input:radio").attr("checked", false);

//     // $('.rating_1 input').click(function () {
//     //     $(".rating_1 span").removeClass('checked');
//     //     $(this).parent().addClass('checked');
//     // });

//     $("input[type='radio'][id='str5_1']").change(
//       function(){
//         var userRating = this.id;
//         alert(userRating);
//     }); 
// });

function g(num,rate) {
    // var userRating = document.getElementById('str5').value;
    // alert(num+" "+rate)
    document.getElementById("disp").value = num+" "+rate;
    }
