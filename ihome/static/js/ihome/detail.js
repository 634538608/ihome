function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {

    var query_data = decodeQuery();
    var house_id = query_data["id"];

    $.get("api/v1.0/detail" + house_id, function (resp) {
        if (resp.errno == 0) {

            img_tmp_html = template("img_html_id", {
                img_urls: resp.data.house_detail["img_urls"],
                price:resp.data.house_detail['price']
            });

            $(".swiper-container").html(img_tmp_html);

            info_tmp_html = template("info_html_id",{
                h_detail:resp.data.house_detail

            });

            $(".detail-con").html(info_tmp_html);

            // /booking.html?id=4
            $(".book-house").attr("href","/booking.html?id="+house_id);

        var mySwiper = new Swiper('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
            if (resp.data.user_id == resp.data.house_detail["user_id"]){
            $(".book-house").hide()
            }

        } else {
            alert(resp.errmsg)
        }
    })



    $(".book-house").show();
})