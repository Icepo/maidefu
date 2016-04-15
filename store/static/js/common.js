/**
 * Created by liuzhangjun on 2016-3-28.
 */
// SPA项目的主体缓存
var cache = {
    "currentItem": {},//当前选中的商品对象
    "addFlag": false,//bind和on会导致自动运行的bug 使用自定义开关控制增加按钮的活性
    "submitFlag": false,//是否可以提交表单
    "selected": {},//当前选择的对象
    "store": {}//当前门店
};
/**
 * 用分页显示的方式实现切换效果
 */
$(document).ready(function () {
    $('#bottom-nav').children().each(function (index) {
        if (index == 0) {
            selectBottom(index);
            $("#page_" + index).css("display", "inherit");
        }
        $(this).bind("touchstart", function () {
            selectBottom(index);
        });
    });
    //绑定AutoComplete输入框
    $("#item-name").bind("keyup", function () {
        if ($(this).val()) {
            setTimeout(autoComplete($(this).val()), 500);
        }
    });
    //绑定AutoComplete的红叉
    $("#input-remove").bind("touchstart", function () {
        $("#item-name").val("");
        $("#list-group").slideUp(200);
        cache.currentItem = {};
    });
    //删除所选条目
    $(".dustbin").on("touchstart", function () {
        var itemRow = $(this).parent();
        Modal.confirm(
            {
                msg: "是否要删除？"
            })
            .on(function (confirm) {
                if (confirm) {
                    itemRow.slideUp(200);
                }
            });
    });
    //增加条目按钮
    $("#add-item-btn").unbind().on("touchstart", function () {
        addItem();
    });
});
/**
 * 增加所选商品到清单
 */
function addItem() {
    if (cache.addFlag) {
        if (cache.selected["pk_" + cache.currentItem.pk]) {
            Modal.alert({
                msg: "商品已经被选择，请直接修改数量即可！"
            });
        } else {
            cache.addFlag = false;
            cache.submitFlag = true;
            addItemToCache();
            $("#add-item-btn").addClass("btn-disabled");
            $("#add-item-btn").attr("disabled", true);
            var newRow = createRow();
            newRow.css("display", "none");
            $("#item-list-" + cache.currentItem.fields.catalog).prepend(newRow);
            newRow.slideDown(200);
            newRow.find(".dustbin").on("touchstart", function () {
                var itemRow = $(this).parent();
                Modal.confirm(
                    {
                        msg: "是否要删除？"
                    })
                    .on(function (confirm) {
                        if (confirm) {
                            removeItemFromCache(itemRow.attr("id"));
                            itemRow.slideUp(200);
                            itemRow.remove();
                        }
                    });
            });
        }
    }
}
function addItemToCache() {
    cache.selected["pk_" + cache.currentItem.pk] = true;
}
function removeItemFromCache(itemId) {
    cache.selected["pk_" + itemId] = undefined;
}
/**
 * 根据当前选择商品创建一行
 */
function createRow() {
    return $('<div class="row list-content" id="' + cache.currentItem.pk + '"><div class="col-xs-5"><span class="list-content-middle list-content-name">' + cache.currentItem.fields.name + '</span></div><div class="col-xs-2"><span class="list-content-middle">' + cache.currentItem.fields.unit + '</span></div><div class="col-xs-3"><input type="text" class="form-control item-list-input list-content-middle" name="' + cache.currentItem.pk + '"></div><div class="col-xs-2 dustbin"><span class="glyphicon glyphicon-trash list-content-middle" aria-hidden="true"></span></div></div>')
}

function autoComplete(text) {
    text = text.trim();
    $.ajax({
        type: "get",
        url: "/store/getItems?text=" + text,
        success: function (data) {
            console.log(data);
            if (data.res_code == "1" && data.res_data.length > 2) {
                var content = "";
                var list = eval(data.res_data);
                for (var i = 0; i < list.length; i++) {
                    var obj = list[i];
                    var keywords = "<css class='keywords'>" + text + "</css>";
                    var name = obj.fields.name;
                    var key_name = name.replace(text, keywords);
                    content += "<button type='button' class='list-group-item' id='" + obj.pk + "' name = " + name + " value='" + obj.fields.unit + "'>" + key_name + "</button>"
                }
                $("#list-group").html(content);
                $("#list-group").slideDown(200);
                $("#list-group").children().each(function (index) {
                    $(this).bind("touchstart", function () {
                        cache.currentItem = list[index];
                        $("#item-name").val($(this).attr("name"));
                        $("#list-group").slideUp(200);
                        $("#add-item-btn").removeAttr("disabled");
                        cache.addFlag = true;
                        $("#add-item-btn").removeClass("btn-disabled");
                    });
                });
            }
        }
    });
}
function selectBottom(currentIndex) {
    $("#bottom-nav").children().each(function (index) {
        if (index == currentIndex) {
            $(this).addClass("selectBottom");
            $("#page_" + index).css("display", "inherit");
        } else {
            $(this).removeClass("selectBottom");
            $("#page_" + index).css("display", "none");
        }
    });
}
function showItems() {
    $("#items").modal("show");
}
/**
 * 请求商品列表
 * 以模态窗口打开
 * 并且绑定选择事件
 * @param catalogId
 */
function showCatalogs(catalogId) {
    if (!cache.currentItems) {
        $.ajax({
            type: "get",
            url: "/store/getItems?catalogId=" + catalogId,
            cache: false,
            success: function (data) {
                console.log(data);
                var items = eval(data.res_data);
                cache.currentItems = items;
                renderCatalogs(items, catalogId);
            }
        });
    } else {
        renderCatalogs(cache.currentItems, catalogId);
    }
}

/**
 * 渲染商品页面
 * @param catalogs
 */
function renderCatalogs(items, catalogId) {
    var content = "";
    for (var i = 0; i < items.length; i++) {
        var obj = items[i];
        content += "<li class='list-group-item' id='" + obj.pk + "'>" + obj.fields.name + "</li>"
    }
    $("#catalogs-row").html(content);
    $("#catalogs").modal("show");
    $("#catalogs-row").children().each(function () {
        $(this).bind("touchstart", function () {
            if ($(this).hasClass("list-group-item-success")) {
                $(this).removeClass("list-group-item-success");
                unSelectItem($(this).attr("id"));
            } else {
                $(this).addClass("list-group-item-success");
                selectItem($(this).attr("id"));
            }
        })
    });
    /*
     绑定选择商品的方法
     最后点击确认的时候才修改内存中的列表
     */
    $("#catalogs button[class='btn-customer']").bind('touchstart', function () {
        console.log(catalogId);
        var cacheKey = "selectItem_" + catalogId;
        var selectedItems = cache[cacheKey].slice(0);
        for (var i = 0; i < cache.currentItems.length; i++) {
            var tempItem = cache.currentItems[i];
            for (var j = 0; j < selectedItems.length; j++) {
                var selectedItem = cache[cacheKey][j];
                if (tempItem.pk == selectedItem.pk) {
                    cache.currentItems.splice(i, 1);
                }
            }
        }
        $(this).unbind("touchstart");
        $("#catalogs").modal("hide");
    });
}

function selectItem(itemId) {
    var cacheKey = "tempItems";
    if (!cache[cacheKey]) {
        cache[cacheKey] = [];
    }
    cache[cacheKey]
}

function unSelectItem(itemId) {
    var cacheKey = "selectItem_" + catalogId;
    for (var i = 0; i < cache[cacheKey].length; i++) {
        var item = cache[cacheKey][i];
        if (item.pk == itemId) {
            cache[cacheKey].splice(item, 1);
        }
    }
}

function selectCatalog(catalogId) {

}
function addCatalog() {
    var currentItemType = "vegetable";
    if ($("#page_2").css("display") == "none") {
        currentItemType = "fruit";
    }
    $.ajax({
        type: "get",
        data: $("#itemCatalogForm").serialize() + "&currentItemType=" + currentItemType + "&temp=" + Math.random(),
        url: "/store/addCatalog",
        cache: false,
        success: function (data) {
            if (data.res_code == "1") {
                $("#success-info").html(data.res_msg);
                $("#success-info").show(500).delay(200).hide(500);
                $("#addCatalog").modal("hide");
                $("#itemCatalogForm")[0].reset();
            } else {
                $("#danger-info").fadeIn(500).delay(200).hide(500);
            }
        },
        error: function () {
            $("#danger-info").fadeIn(500).delay(200).hide(500);
        }
    });

}
function confirmSubmit() {
    var selectNum = Object.getOwnPropertyNames(cache.selected).length;
    if (selectNum > 0) {
        Modal.confirm({
            msg: '共选择了[' + selectNum + ']件商品，是否确认提交？'
        }).on(function (confirm) {
            if (confirm) {
                $.loading.show();
                submitItems();
            }
        });
    } else {
        Modal.alert({
            msg: "您还没选择商品"
        })
    }
}
/**
 * 点击报货按钮
 */
function submitItems() {
    var reg = /^\d+(\.\d+)?$/;
    var inputs = $("#item-form").find("input");
    for (var i = 0; i < inputs.length; i++) {
        var inputObj = $(inputs[i]);
        var num = inputObj.val();
        var name = inputObj.parent().parent().find(".list-content-name").html();
        console.log(name);
        if (num && num.match(reg)) {
            console.log(true);
        } else {
            console.log(false);
            $.loading.hide();
            Modal.alert({
                msg: "[" + name + "] 的数目格式不正确，请核实！"
            });
            return false;
        }
    }
    var values = JSON.stringify($("#item-form").serializeArray());
    cache.open_id = "test_open_id";
    cache.nick_name = "test_nick_name";
    var countor = JSON.stringify({
        "ALLOW_TIME_1": $("#item-list-1").children().length,
        "ALLOW_TIME_2": $("#item-list-2").children().length,
        "ALLOW_TIME_3": $("#item-list-3").children().length,
        "ALLOW_TIME_4": $("#item-list-4").children().length,
        "ALLOW_TIME_5": $("#item-list-5").children().length
    });
    if (cache.open_id && cache.nick_name) {
        var content = {
            "open_id": cache.open_id,
            "nick_name": cache.nick_name,
            "values": values,
            "counter": countor
        };
        console.log(content);
        $.ajax({
            type: "POST",
            url: "/store/daily",
            data: content,
            success: function (data) {
                $.loading.hide();
                Modal.alert({
                    msg: data.res_msg
                })
            },
            error: function (data) {
                $.loading.hide();
                Modal.alert({
                    msg: '出错了！！！'
                })
            }
        });
    }
}

//选择门店方法
function selectStore(id) {
    Modal.confirm(
        {
            msg: "请输入密码:<br><input type='text' id='storepwd'/>"
        })
        .on(function (confirm) {
            if (confirm) {
                $.ajax({
                    type: "post",
                    url: "/store/checkStore",
                    data: '{"id":' + id + ',"pwd":"' + $("#storepwd").val() + '"}',
                    success: function (data) {
                        console.log(data)
                    }
                })
            }
        });
}