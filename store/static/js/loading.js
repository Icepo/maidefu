$(function () {
    var loading = '<div id="loading-mask" class="loading-mask"></div><div id="loading-content" class="loading-content"></div>';

    $("body").append(loading);
    jQuery.loading = {
        "show": function () {
            $("#loading-mask").css("height", $(window).height());
            $("#loading-mask").css("display", "inherit");
            $("#loading-content").css("display", "inherit");
        },
        "hide": function () {
            $("#loading-mask").css("display", "none");
            $("#loading-content").css("display", "none");
        }
    }
});