//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-accept").attr("order-id", orderId);
    });
    $(".order-reject").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-reject").attr("order-id", orderId);
    });

    $.ajax({
        url:"api/v1.0/lorder",
        type:"get",
        dataType:"json",
        header:{
            "X-CSRFToken":getCookie('csrf_token')
        },
        success:function (resp) {
            if(resp.errno==4102){
                alert("请登录");
                location.href="/login.html"
            }
            if(resp.errno==0){
               $(".orders-list").html(template("lorder_html_id", {orders:resp.data.orders}))
            }else {
                alert(resp.errmsg)
            }

        }
    });

    $(".modal-accept").click(function () {
        //确定接单
        var orderId = $("#my_order_id").attr("order-id");
        $.ajax({
            url:"/api/v1.0/accept_order"+orderId,
            type:"put",
            dataType:"json",
            header:{
                'X-CSRFToken':getCookie("csrf-token")
            },
            success:function (resp) {
                if(resp.errno==0){
                    alert('接单成功！')
                    location.href='/lorders.html'
                }

                else {
                    alert(resp.errmsg)
                }

            }
        });
    })
    $(".modal-reject").click(function () {
        //确定拒单
        var orderId = $("#my_order_id").attr("order-id");
        var refuse_reason = $("#reject-reason").val();

        $.ajax({
             url:"/api/v1.0/refuse_order"+orderId,
            type:"put",
            data:JSON.stringify({"refuse_reason":refuse_reason}),
            contentType:'application/json',
            dataType:"json",
            header:{
                'X-CSRFToken':getCookie("csrf-token")
            },
            success:function (resp) {
                if(resp.errno==0){
                    alert('拒单成功！');
                    location.href='/lorders.html'

                }

                else {
                    alert(resp.errmsg)
                }

            }
        });
    })

});