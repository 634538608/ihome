function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function myDecodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function MyDecodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

// $(document).ready(function () {
//
//     $(".input-daterange").datepicker({
//         format: "yyyy-mm-dd",
//         startDate: "today",
//         language: "zh-CN",
//         autoclose: true
//     });
//     $(".input-daterange").on("changeDate", function () {
//         var startDate = $("#start-date").val();
//         var endDate = $("#end-date").val();
//
//         if (startDate && endDate && startDate > endDate) {
//             showErrorMsg();
//         } else {
//             var sd = new Date(startDate);
//             var ed = new Date(endDate);
//             var days = (ed - sd) / (1000 * 3600 * 24) + 1;
//             var price = $(".house-text>p>span").html();
//             var amount = days * parseFloat(price);
//             $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
//         }
//     });
//
//
//     var query_data = MyDecodeQuery();
//     var house_id = query_data["id"];
//     $.get("api/v1.0/booking?" + house_id, function (resp) {
//
//         if (resp.errno == 0) {
//             tmp_html = template("booking_html_id", {house: resp.data.house});
//             $(".house-info").html(tmp_html)
//         } else {
//             alert(resp.errmsg)
//         }
//
//
//     })
//
//     var booking_data = {
//         "house_id": house_id,
//         "start_date": $("#start-date").val(),
//         "end_date": $("#end-date").val(),
//         "days":days,
//         "price":price,
//
//
//     }
//     $(".submit-btn").click(function () {
//         $.ajax({
//             url: "api/v1.0/real_booking",
//             type:"post",
//             data:booking_data,
//             contentType:"application/json",
//             dataType:"json",
//             header:{
//                 "X-CSRFToken":getCookie('csrf-token')
//             },
//             success:function (resp) {
//                 if (resp.errno==4102){
//                     location.herf = 'login.html'
//                 }
//                 if (resp.errno==0){}
//                 else {
//                     alert(resp.errmsg)
//                 }
//
//             }
//
//         })
//
//     })
//
//
// })


$(document).ready(function () {

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });


    $(".input-daterange").on("changeDate", function () {
        startDate = $("#start-date").val();
        endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd) / (1000 * 3600 * 24) + 1;
            price = $(".house-text>p>span").html();
            amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
        }
    });


    var query_data = MyDecodeQuery();
    var house_id = query_data["id"];
    $.get("api/v1.0/booking" + house_id, function (resp) {

        if (resp.errno == 0) {
            tmp_html = template("booking_html_id", {house: resp.data.house});
            $(".house-info").html(tmp_html)
        } else {
            alert(resp.errmsg)
        }


    });

    $(".submit-btn").click(function () {

          var sd = new Date($("#start-date").val());
            var ed = new Date($("#end-date").val());
            var days = (ed - sd) / (1000 * 3600 * 24) + 1;
            var price = $(".house-text>p>span").html()
            var booking_data = {
                "house_id": house_id,
                "start_date": $("#start-date").val(),
                "end_date": $("#end-date").val(),
                "days": days,
                "price": price,
                "amount": days * parseFloat(price)
            };


            $.ajax({
                url: "api/v1.0/real_booking",
                type: "post",
                data: JSON.stringify(booking_data),
                contentType: "application/json",
                dataType: "json",
                header: {
                    "X-CSRFToken": getCookie('csrf-token')
                },
                success: function (resp) {
                    if (resp.errno == 4102) {
                        location.href= '/login.html'
                    }
                    if (resp.errno == 0) {
                        alert("成功预定！");
                        location.href = '/orders.html';


                    }
                    else {
                        alert(resp.errmsg)
                    }

                }

            })




    })


})