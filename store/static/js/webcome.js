/**
 * Created by liuzhangjun on 2016-4-13.
 * 登录页面
 */
$(function () {
    $("#login").on("touchstart", function () {
        do_login();
    });
});
/*登录*/
function do_login() {
    var name = $("#name").val();
    var pwd = $("#pwd").val();
    if (!name || name == "") {
        Modal.alert({
            msg: '请输入用户名！'
        });
        return;
    }
    if (!pwd || pwd == "") {
        Modal.alert({
            msg: '请输入密码'
        });
        return;
    }
    $.loading.show();
    $.ajax({
        type: "POST",
        data: $("#login-form").serializeArray(),
        url: 'store/login',
        success: function (data) {
            $.loading.hide();
            console.log(data);
            if (data.res_code == "1") {
                window.location.href = "store/mobile"
            } else {
                Modal.alert({
                    msg: data.res_msg
                })
            }
        },
        error: function (data) {
            $.loading.hide();
            console.log(data);
            Modal.alert({
                msg: "后台出错了！！！"
            });
        }
    });
}