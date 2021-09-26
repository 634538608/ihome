function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {


    $.ajax({
        url:'/api/v1.0/logout',
        type:'delete',
        header:{
           'X-SCRFToken':getCookie('scrf-token')
        },
        success:function (resp) {
            if(resp.errno==0){
                alert('已退出！');
                location.href='/';
            }

        }
    })

}

function check_auth() {
     $.ajax({
        url:'/api/v1.0/auth',
        type:'get',
        dataType:'json',
        header:{
            'X-SCRFToken':getCookie('csrf_token')
        },
        success:function (resp) {
            if(resp.errno==4102){
                   location.href='/login.html'
                }
            if(resp.errno==0){
                location.href="/my.html";
                alert('已经实名验证！')
            }
        }

    });
}



$(document).ready(function () {
            $.ajax({
            url: "/api/v1.0/my",
            type: 'get',
            dataType: 'json',
            header: {
                "X-CSRFToken": getCookie('csrf_token')
            },
            success: function (resp) {
                if(resp.errno==4102){
                    location.href='/login.html'
                }
                if (resp.errno == 0) {
                    $("#user-avatar").attr('src',resp.data.avatar_url);
                    $("#user-name").html(resp.data.user_name);
                    $("#user-mobile").html(resp.data.mobile);

                } else {

                    alert(resp.errmsg)
                }

            }
        })




})