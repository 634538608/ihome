var cur_page = 1; // 当前页
var next_page = 1; // 下一页
var total_page = 1;  // 总页数
var house_data_querying = true;


function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}

function update_house_data1(action) {
    alert("up_house_data")
    var params = {
        "sd": $("#start-date").val(),
        'ed': $("#end-date").val(),
        'aid': $("#area_li_id").attr("area-id"),
        'sort': $(".filter-sort>li.active").attr("sort-key"),
        'page': next_page

    }

    $.get("/api/v1.0/search_house", params, function (resp) {
        if (resp.errno == 0) {
            if (0 == resp.data.total_page) {
                $(".house-list").html("暂时没有符合您查询的房屋信息。");
            } else {
                total_page = resp.data.total_page;
                if ("review" == action) {
                    cur_page = 1;
                    $(".house-list").html(template("house_html_id", {
                        houses: resp.data.houses,
                        total_page: resp.data.total_page,
                        current_page: resp.data.current_page,
                    }))

                } else {
                    cur_page = next_page;
                    $(".house-list").append(template("house_html_id", {
                        houses: resp.data.houses,
                        total_page: resp.data.total_page,
                        current_page: resp.data.current_page,
                    }))
                }
            }
        } else {
            alert(resp.errmsg)
        }

    })
}

function update_house_data() {
    // alert("up_house_data")
    var params = {
        "sd": $("#start-date").val(),
        'ed': $("#end-date").val(),
        'aid': $("#area_li_id").attr("area-id"),
        'sort': $(".filter-sort>li.active").attr("sort-key"),
        'page': next_page

    }

    $.get("/api/v1.0/search_house", params, function (resp) {
            // resp = JSON.stringify(resp);

        if (resp.errno == 0) {
            if (0 == resp.data.total_page) {
                $(".house-list").html("暂时没有符合您查询的房屋信息。");
            } else {
                // alert("template")

                tmp_html=template("house_html_id", {
                    houses: resp.data.houses,
                    total_page: resp.data.total_page,
                    current_page: resp.data.current_page
                })
                $(".house-list").html(tmp_html)
            }
        } else {
            alert(resp.errmsg)
        }

    })
}

$(document).ready(function () {
    // alert(1);

    // update_house_data("renew");


    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);


    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function (e) {
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function (e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();

    });
    $(".filter-item-bar>.filter-area").on("click", "li", function (e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function (e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    })


    $.get('/api/v1.0/areas', function (resp) {
        if (resp.errno == 0) {
            // alert(resp.data.areas);
            tmp_html = template('areas_tmp', {areas: resp.data.areas})
            $(".filter-area").html(tmp_html);

            $(".area-list a").click(function (e) {
                $("#area-btn").html($(this).html());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).html());
                $("#area-modal").modal("hide");


                // update_house_data("renew");


            });

        } else {
            alert(resp.errmsg)
        }

    });


    $(".display-mask").on("click", function (e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        // update_house_data("renew");

    });

    update_house_data();

})