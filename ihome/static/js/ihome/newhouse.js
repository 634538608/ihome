function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {


    $.get('/api/v1.0/areas', function (resp) {
        if (resp.errno == 0) {
            tmp_html = template('areas_tmp', {areas: resp.data.areas})
            $(".form-control").html(tmp_html);


        } else {
            alert(data.errmsg)
        }

    });

    $("#form-house-info").submit(function (e) {
        e.preventDefault();
        var house_data = {};
        var fly_data = [];
        $("#form-house-info").serializeArray().map(function (x) {
            house_data[x.name] = x.value
        });
        $(":checked[name=facility]").each(function (index, x) {
            fly_data[index] = $(x).val()
        });
        house_data['facilities'] = fly_data;

        $.ajax({
            url: "api/v1.0/new_house",
            type: 'post',
            data: JSON.stringify(house_data),
            contentType: 'application/json',
            dataType: 'json',
            header: {
                "X-CSRFToken": getCookie('csrf-token')
            },
            success: function (resp) {
                if (resp.errno == 4102) {
                    location.href = 'login/html'
                }
                if (resp.errno == 0) {
                    $("#house-id").attr("value", resp.data.house_id);
                    $('.popup_con').fadeIn('fast');
                    $('.popup_con').fadeOut('fast');
                    $("#form-house-info").hide();
                    $("#form-house-image").show();
                } else {
                    alert(resp.errmsg)

                }
            }
        })


    })

    $("#form-house-image").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: 'api/v1.0/house_img',
            type: 'post',
            dataType: 'json',
            header: {"X-CSRFToken": getCookie('csrf_token')},
            success: function (resp) {
                if (resp.errno == 4102) {
                    location.href = '/login.html'
                }
                if (resp.errno == 0) {
                    $(".house-image-cons").append('<img src="' + resp.data.image_url + '">');
                    alert("保存成功！")
                }
                else {
                    alert(resp.errmsg)
                }
            }
        })
    })

})