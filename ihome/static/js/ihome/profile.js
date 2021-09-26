function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$("#form-avatar").submit(function (e) {
    e.preventDefault();
    $(this).ajaxSubmit({
        url: '/api/v1.0/profile_photo',
        type: 'post',
        dataType: 'json',
        header: {
            'X-SCRFToken': getCookie('csrf_token')
        },
        success: function (resp) {
            if (resp.errno == 4102) {
                location.href = '/login.html'
            }
            if (resp.errno == 0) {
                $("#user-avatar").attr('src', resp.data.avatar)
                showSuccessMsg();
            } else {
                alert(resp.errmsg)
            }

        }
    })
});
$("#form-name").submit(function (e) {
    e.preventDefault();
    var req_data = {'user_name': $("#user-name").val()};
    $.ajax({
        url: 'api/v1.0/user_name',
        type: 'post',
        data: JSON.stringify(req_data),
        contentType: 'application/json',
        dataType: 'json',
        header: {
            "X-CSRFToken": getCookie('csrf_token')
        },
        success: function (resp) {
            if (resp.errno == 0) {
                $("#user-name").attr('value', resp.data.user_name);
                showSuccessMsg();

            } else {
                alert(resp.errmsg)
            }

        }
    })
});

$(document).ready(function () {
    $.ajax({
        url: 'api/v1.0/profile',
        type: 'get',
        dataType: 'json',
        header: {
            'X-CSRFToken': getCookie('csrf_token')
        },
        success: function (resp) {
            if (resp.errno==4102) {
                location.href='/login.html'
            }
            if (resp.errno == 0) {
                $("#user-name").attr('value', resp.data.user_name);
                $("#user-avatar").attr('src', resp.data.avatar_url);
                // location.href='/my.html'
            }
        }
    })
});