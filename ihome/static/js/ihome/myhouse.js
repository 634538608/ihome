function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function () {


    $.ajax({
        url: '/api/v1.0/auth',
        type: 'get',
        dataType: 'json',
        header: {
            'X-SCRFToken': getCookie('csrf_token')
        },
        success: function (resp) {
            if (resp.errno == 4102) {
                location.href = '/login.html'
            }
            if (resp.errno == 0) {


                $.ajax({
                    url: "api/v1.0/my_house",
                    type: 'get',
                    dataType: "json",
                    header: {
                        'X-SCRFToken': getCookie('csrf_token')
                    },
                    success: function (resp) {
                        if (resp.errno == 4102) {
                            location.href = '/login.html'
                        }
                        if (resp.errno == 0) {
                            // alert(resp.data.houses);
                            tmp_html=template("tmp_html_id",{house_li:resp.data.houses});
            //                 house_html=template("house_tmp_id",{houses:resp.data.data})
            // $("#houses-list").find("li").eq(0).append(house_html)
                            // $("#houses-list").html(tmp_html)
                            $("#houses-list").find("li").eq(0).append(tmp_html)
                        }else {
                            alert(resp.errmsg)
                        }
                    }
                })



            } else {
                $(".auth-warn").show();
                $(".new-house").hide();
            }
        }

    });


});

