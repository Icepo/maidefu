"""maidefu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from store.views import add_catalog, import_data, get_items, daily, admin_login, \
    admin_index, check_store, store_list, query_items, back_login, welcome_page, store_login, mobile_index, \
    back_welcome_page, error_page, back_index, back_report, item_manager, new_item, del_item, store_manager, new_store, \
    del_store, staff_manager, new_staff, del_staff, query_staff_store

urlpatterns = [
    url(r'^$', welcome_page),
    url(r'^admin/', admin.site.urls),
    url(r'^store$', welcome_page),
    url(r'^store/login$', store_login),
    url(r'^store/mobile$', mobile_index),
    url(r'^store/adminLogin$', admin_login),
    url(r'^store/index$', admin_index),
    url(r'^store/addCatalog/*$', add_catalog),
    url(r'^store/getItems/*$', get_items),
    url(r'^store/importData$', import_data),
    url(r'^store/daily$', daily),
    url(r'^store/checkStore$', check_store),
    url(r'^store/storeList$', store_list),
    url(r'^store/back/login$', back_login),
    url(r'^back$', back_welcome_page),
    url(r'^back/adminLogin$', admin_login),
    url(r'^back/error$', error_page),
    url(r'^back/index$', back_index),
    url(r'^back/report$', back_report),
    url(r'^back/queryItems$', query_items),
    url(r'^back/itemManager$', item_manager),
    url(r'^back/newItem$', new_item),
    url(r'^back/delItem$', del_item),
    url(r'back/storeManager$', store_manager),
    url(r'back/newStore', new_store),
    url(r'back/delStore', del_store),
    url(r'back/staffManager$', staff_manager),
    url(r'back/newStaff', new_staff),
    url(r'back/delStaff', del_staff),
    url(r'back/queryStaffStore', query_staff_store)

]
