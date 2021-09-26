//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);


    $(".order-comment").on("click", function () {
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });

    $.ajax({
        url: "/api/v1.0/orders",
        type: "get",
        dataType: "json",
        header: {
            "X-CSRFToken": getCookie('csrf-token')
        },
        success: function (resp) {
            if (resp.errno == 4102) {
                location.href = '/login.html'
            }
            if (resp.errno == 0) {
                $(".orders-list").html(template("orders-list-tmpl", {orders: resp.data.orders}))

                $(".order-pay").on("click", function () {

                    var order_id = $(this).attr("order-id");
                    $.ajax({
                        url: "/api/v1.0/pay_message" + order_id,
                        type: "get",
                        dataType: "json",
                        header: {
                            "X-SCRFToken": getCookie('csrf-token')
                        },
                        success: function (resp) {
                            if (resp.errno == 4102) {
                                location.href = '/login.html'
                            }
                            if (resp.errno == 0) {
                                alert(resp.data.alipay_url)
                                location.href = resp.data.alipay_url
                            } else {
                                alert(resp.errmsg)
                            }

                        }
                    })
                })


            }


        }
    })

});
























