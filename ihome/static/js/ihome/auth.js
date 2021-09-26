function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {



    $("#form-auth").submit(function (e) {
        e.preventDefault();
        var req_data = {
            'real_name':$('#real-name').val(),
            'id_card':$('#id-card').val()
        };
        // alert(req_data);
        $.ajax({
            url:'/api/v1.0/user_auth',
            type:'post',
            data:JSON.stringify(req_data),
            contentType:'application/json',
            dataType:'json',
            header:{
             'X-SCRFToken':getCookie('csrf_token')
            },
            success:function (resp) {
                // alert(resp.errno);
                if(resp.errno==4102){
                   location.href='/login.html'
                }
                if(resp.errno==0){
                   showSuccessMsg();
                   location.href='/my.html'
                }else {
                    alert(resp.errmsg)
                }

            }
        })

    });



});