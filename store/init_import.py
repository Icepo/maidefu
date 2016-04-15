# coding=utf-8
import xlrd

from store.models import Item, Catalog, Store, Staff, StaffStoreRel


def import_items():
    catalogs = [u'水果', u'蔬菜', u'副食', u'双汇冷鲜肉', u'熟食']
    root_path = u'E:/龙兄的门店/'
    for name in catalogs:
        path = root_path + name + '.xls'
        wb = xlrd.open_workbook(path)
        table = wb.sheets()[0]
        total_row = table.nrows
        print total_row
        for i in range(1, total_row):
            print path, table.cell_value(i, 0), table.cell_value(i, 1), table.cell_value(i, 2), total_row, i
            Item.objects.create(name=table.cell_value(i, 0), unit=table.cell_value(i, 1), sts="A",
                                catalog_id=table.cell_value(i, 2))
        Catalog.objects.create(name=name, sts='A')


def import_stores():
    path = u'E:/龙兄的门店/新数据/麦德福连锁编号-1.xls'
    wb = xlrd.open_workbook(path)
    table = wb.sheets()[0]
    total_row = table.nrows
    print total_row
    for i in range(1, total_row):
        store_id = table.cell_value(i, 0)
        name = table.cell_value(i, 1)
        manager = table.cell_value(i, 2)
        mobile = table.cell_value(i, 3)
        if mobile:
            mobile = str(mobile)[:-2]
        tel = table.cell_value(i, 4)
        if tel:
            tel = str(tel)[:-2]
        addr = table.cell_value(i, 5)
        print store_id, name, manager, mobile, tel, addr, i, total_row
        Store.objects.create(store_id=store_id, store_name=name, store_manager=manager, store_mobile=mobile,
                             store_tel=tel,
                             store_addr=addr)


def import_staff():
    path = u'E:/龙兄的门店/新数据/麦德福连锁编号-1.xls'
    wb = xlrd.open_workbook(path)
    table = wb.sheets()[0]
    total_row = table.nrows
    print total_row
    for i in range(1, total_row):
        store_id = table.cell_value(i, 0)
        name = table.cell_value(i, 1)
        manager = table.cell_value(i, 2)
        mobile = table.cell_value(i, 3)
        if mobile:
            mobile = str(mobile)[:-2]
        tel = table.cell_value(i, 4)
        if tel:
            tel = str(tel)[:-2]
        addr = table.cell_value(i, 5)
        print store_id, name, manager, mobile, tel, addr
        staff = Staff.objects.create(open_id='temp_open_id', real_name=manager, mobile_num='18600000000',
                                     sts='A',
                                     password='123456')
        StaffStoreRel.objects.create(staff_id=staff.id, store_id=i, sts='A')
        print i
