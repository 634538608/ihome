function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

    var rep_data={
           "mobile":mobile,
            "passwd":passwd,
            "X-CSRFToken":getCookie('csrf-token')
    };
    rep_data = JSON.stringify(rep_data);
        $.ajax({
            url:"/api/v1.0/login",
            type:'post',
            data:rep_data,
            contentType:"application/json",
            dataType:'json',
            header:{
                "X-CSRFToken":getCookie('csrf-token')
            },

            success:function (resp) {
                if(resp.errno==4104||resp.errno==0){
                    location.href="/";
                }else {
                    alert(resp.errmsg);
                }

            }
        })

    });
})