# coding=utf-8
import datetime
import json
import logging
import time

from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from store.init_import import import_staff
from store.models import Item, DaliyDetail, Staff, DaliyBatch, Store, SysConfig, Catalog, StaffStoreRel

logger = logging.getLogger(__name__)


# 欢迎页
def welcome_page(request):
    logger.info('store/webcome_page.html')
    return render(request, 'store/webcome_page.html')


# 前端的登录
@csrf_exempt
def store_login(request):
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    logger.info('name:' + name + ',' + 'pwd:' + pwd)
    staff_set = Staff.objects.filter(real_name=name, password=pwd, sts='A')
    if staff_set.exists():
        staff = staff_set.first()
        store_set = Store.objects.filter(store_staff_rel__staff=staff.id, sts='A', store_staff_rel__sts='A')
        if store_set.exists():
            store = store_set.first()
            request.session["staff_id"] = staff.id
            request.session["staff_name"] = staff.real_name
            request.session["store_id"] = store.store_id
            request.session["store_name"] = store.store_name
            request.COOKIES["store_id"] = store.store_id
            request.COOKIES["staff_id"] = staff.id
            return JsonResponse({"res_code": "1", "res_msg": u"操作成功"})
        else:
            msg = u"未找到与该员工匹配的门店"
    else:
        msg = u"不存在这个用户"
    return JsonResponse({"res_code": "0", "res_msg": msg})


# 移动端主页
def mobile_index(request):
    content = {"store_name": request.session["store_name"], "staff_name": request.session["staff_name"],
               "items": Item.objects.all().filter(sts='A')}
    logger.info(content)
    return render(request, 'store/base.html', content)


# 模糊查找商品
def get_items(request):
    text = request.GET["text"]
    logger.info(text)
    return JsonResponse(
            {"res_code": "1", "res_msg": u"操作成功",
             "res_data": serializers.serialize("json", Item.objects.filter(name__contains=text))})


# 报货
@csrf_exempt
def daily(request):
    # 检查时间
    time_check = right_time(request.POST["counter"])
    if time_check:
        store_id = request.session.get("store_id")
        if store_id:
            values = json.loads(request.POST["values"])
            open_id = request.POST["open_id"]
            nick_name = request.POST["nick_name"]
            last_post = request.session.get("last_post", default=None)
            # 有上次报货时间的情况下需要验证下上次报货时间差
            if last_post:
                time_passed = 60 - (time.mktime(datetime.datetime.now().timetuple()) - last_post)
                if time_passed > 0:
                    result_dict = {"res_code": "0", "res_msg": u"每分钟只可以提交一次报货，请稍后操作!，还有 " + str(time_passed) + u"秒"}
                    return JsonResponse(result_dict)
            daliy_bath = DaliyBatch.objects.create(open_id=open_id, nick_name=nick_name, store_id=store_id,
                                                   total=len(values),
                                                   sts='A')
            logger.info("create bath success")
            for item in values:
                DaliyDetail.objects.create(open_id=open_id, nick_name=nick_name, store_id=store_id,
                                           item_id=item["name"],
                                           num=item["value"], batch_id=daliy_bath.id, sts='A')
            request.session["last_post"] = time.mktime(datetime.datetime.now().timetuple())
            result_dict = {"res_code": "1", "res_msg": u"操作成功"}
        else:
            result_dict = {"res_code": "0", "res_msg": u"没有找到所属门店，请联系管理员"}
    else:
        result_dict = {"res_code": "0", "res_msg": time_check}
    logger.info(result_dict)
    return JsonResponse(result_dict)


# 检查报货时间 通过返回true 否则返回错误信息
def right_time(counter_str):
    current = datetime.datetime.now().strftime('%H:%M')
    counter = json.loads(counter_str)
    if counter["ALLOW_TIME_1"] != 0:
        fruit_config = SysConfig.objects.filter(config_code="ALLOW_TIME_1", sts="A").first().config_value
        if current > fruit_config:
            return u"水果的报货时间为" + fruit_config + u"之前"
    if counter["ALLOW_TIME_2"] != 0:
        fruit_config = SysConfig.objects.filter(config_code="ALLOW_TIME_2", sts="A").first().config_value
        if current > fruit_config:
            return u"蔬菜的报货时间为" + fruit_config + u"之前"
    if counter["ALLOW_TIME_3"] != 0:
        fruit_config = SysConfig.objects.filter(config_code="ALLOW_TIME_3", sts="A").first().config_value
        if current > fruit_config:
            return u"副食的报货时间为" + fruit_config + u"之前"
    if counter["ALLOW_TIME_4"] != 0:
        fruit_config = SysConfig.objects.filter(config_code="ALLOW_TIME_4", sts="A").first().config_value
        if current > fruit_config:
            return u"双汇冷鲜肉的报货时间为" + fruit_config + u"之前"
    if counter["ALLOW_TIME_5"] != 0:
        fruit_config = SysConfig.objects.filter(config_code="ALLOW_TIME_5", sts="A").first().config_value
        if current > fruit_config:
            return u"熟食的报货时间为" + fruit_config + u"之前"
    return True


# 后台登录页面
def back_welcome_page(request):
    logger.info('back/login.html')
    return render(request, 'back/login.html')


# 后台错误页面
def error_page(request):
    logger.info('back/error.html')
    return render(request, 'back/error.html')


# 后台登录
@csrf_exempt
def admin_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    logger.info(username + "," + password)
    if username and password:
        staff_set = Staff.objects.filter(real_name=username, password=password, sts='S')
        if staff_set.exists():
            staff = staff_set.first()
            request.session["staff_id"] = staff.id
            request.session["staff_name"] = staff.real_name
            logger.info("login success")
            return HttpResponseRedirect('/back/index')
    return HttpResponseRedirect('/back/error')


# 后台主页
def back_index(request):
    logger.info("back/index.html")
    username = request.session.get("staff_name")

    return render_to_response('back/index.html', {"username": username})


# 后台清单模板
def back_report(request):
    logger.info("back_report")
    stores = Store.objects.all().filter(sts='A')
    return render_to_response("back/commponent/report.html", {"stores": stores})


# 查询指定门店和日期的货品列表
@csrf_exempt
def query_items(request):
    target_date = request.GET.get("target_date")
    query_stores = request.GET.get("query_stores")
    raw_sql = "select b.id, SUM(a.num) num,b.name, b.unit from store_daliydetail a, store_item b where a.item_id=b.id AND a.create_date LIKE %s AND a.store_id in (" + query_stores + ") GROUP BY b.id, b.name, b.unit"
    raw_querySet = Item.objects.raw(raw_sql, [r'%' + target_date + '%'])
    res_str = ""
    if raw_querySet:
        index = 1
        for raw_obj in raw_querySet:
            res_str = res_str + "<tr><td>" + str(
                    index) + "</td><td>" + raw_obj.name + "</td><td>" + raw_obj.unit + "</td><td>" + str(
                    raw_obj.num) + "</td><td></td><td></td><td></td><td></td></tr>"
            index = index + 1
    result_dict = {"res_code": "1", "res_msg": u"操作成功",
                   "res_data": res_str}
    return JsonResponse(result_dict)


# 货品管理页面
def item_manager(request):
    logger.info("item_manager")
    catalogs = Catalog.objects.all().filter(sts='A')
    items = Item.objects.all().filter(sts='A')
    return render_to_response("back/commponent/item_manager.html", {"catalogs": catalogs, "items": items})


# 新增商品 或者修改商品
@csrf_exempt
def new_item(request):
    item_id = request.POST.get("item_id")
    item_name = request.POST.get("item_name")
    item_unit = request.POST.get("item_unit")
    item_catalog = request.POST.get("item_catalog")
    if item_id is u'':
        Item.objects.create(name=item_name, unit=item_unit, sts="A",
                            catalog_id=item_catalog)
        msg = u"增加操作成功"
    else:
        Item.objects.filter(id=int(item_id)).update(name=item_name, unit=item_unit, sts="A",
                                                    catalog_id=item_catalog, sts_date=datetime.datetime.now())
        msg = u"修改成功"
    result_dict = {"res_code": "1", "res_msg": msg}
    return JsonResponse(result_dict)


# 删除商品
def del_item(request):
    item_id = request.GET.get("item_id")
    Item.objects.filter(id=int(item_id)).update(sts="P", sts_date=datetime.datetime.now())
    result_dict = {"res_code": "1", "res_msg": u'成功删除'}
    return JsonResponse(result_dict)


# 门店管理
def store_manager(request):
    logger.info("store_manager")
    stores = Store.objects.all().filter(sts='A')
    return render_to_response("back/commponent/store_manager.html", {"stores": stores})


# 新增门店
@csrf_exempt
def new_store(request):
    store_id = request.POST.get("store_id")
    store_name = request.POST.get("store_name")
    store_manager = request.POST.get("store_manager")
    store_mobile = request.POST.get("store_mobile")
    store_tel = request.POST.get("store_tel")
    store_addr = request.POST.get("store_addr")
    if store_id is u'':
        Store.objects.create(store_name=store_name, store_manager=store_manager, store_mobile=store_mobile,
                             store_tel=store_tel, store_addr=store_addr, sts='A')
        msg = u"增加操作成功"
    else:
        Store.objects.filter(store_id=int(store_id)).update(store_name=store_name, store_manager=store_manager,
                                                            store_mobile=store_mobile,
                                                            store_tel=store_tel, store_addr=store_addr, sts='A')
        msg = u"修改成功"
    result_dict = {"res_code": "1", "res_msg": msg}
    return JsonResponse(result_dict)


# 删除门店
def del_store(request):
    store_id = request.GET.get("item_id")
    Store.objects.filter(id=int(store_id)).update(sts="P", sts_date=datetime.datetime.now())
    result_dict = {"res_code": "1", "res_msg": u'成功删除'}
    return JsonResponse(result_dict)


# 门店员工
def staff_manager(request):
    logger.info("store_manager")
    staffs = Staff.objects.all().filter(sts='A')
    stores = Store.objects.all().filter(sts='A')
    return render_to_response("back/commponent/staff_manager.html", {"staffs": staffs, "stores": stores})


# 新增员工
@csrf_exempt
def new_staff(request):
    staff_id = request.POST.get("staff_id")
    real_name = request.POST.get("real_name")
    mobile_num = request.POST.get("mobile_num")
    checked_store = request.POST.get("checked_store")
    if staff_id is u'':
        Staff.objects.create(real_name=real_name, mobile_num=mobile_num, open_id="test_open_id", sts='A')
        msg = u"增加操作成功"
    else:
        Staff.objects.filter(id=int(staff_id)).update(real_name=real_name, mobile_num=mobile_num, sts='A')
        if checked_store:
            StaffStoreRel.objects.filter(staff_id=int(staff_id)).update(store_id=checked_store)
        msg = u"修改成功"
    result_dict = {"res_code": "1", "res_msg": msg}
    return JsonResponse(result_dict)


# 删除员工
def del_staff(request):
    staff_id = request.GET.get("staff_id")
    Staff.objects.filter(id=int(staff_id)).update(sts="P", sts_date=datetime.datetime.now())
    result_dict = {"res_code": "1", "res_msg": u'成功删除'}
    return JsonResponse(result_dict)


def query_staff_store(request):
    staff_id = request.GET.get("staff_id")
    stores = Store.objects.filter(store_staff_rel__staff_id=staff_id)
    if stores.exists():
        store_id = stores.first().store_id
        result_dict = {"res_code": "0", "res_msg": u'操作成功', "res_data": store_id}
    return JsonResponse(result_dict)


# 初始化数据
def import_data(request):
    # import_items()
    # import_stores()
    import_staff()
    result_dict = {"res_code": "1", "res_msg": u"操作成功"}
    return JsonResponse(result_dict)


# 后台管理主页
def admin_index(request):
    username = request.COOKIES.get("username")
    return render_to_response("store/templates/admin/index.html", {'username': username})


# 设置门店
@csrf_exempt
def check_store(request):
    if request.method == 'POST':
        store_id = request.POST.get("store_id")
        pwd = request.POST.get["pwd"]
        if id and pwd:
            store = Store.objects.filter(store_id=store_id, store_mobile=pwd, sts='A')
            if store:
                result_dict = {"res_code": "1", "res_msg": u"操作成功", "data": json.dumps(store)}
                return JsonResponse(result_dict)


# 查询门店列表
def store_list(request):
    store_list = Store.objects.all().filter(sts='A')
    result_dict = {"res_code": "1", "res_msg": u"操作成功",
                   "res_data": serializers.serialize("json", store_list)}
    return JsonResponse(result_dict)


# 管理后台的登录方法 针对PC端
def back_login(request):
    return render(request, 'back/login.html')


def add_catalog(request):
    print request.GET["itemCatalog"]
    print request.GET["itemUnit"]
    print request.GET["currentItemType"]
    result_dict = {"res_code": "1", "res_msg": u"操作成功"}
    return JsonResponse(result_dict)
