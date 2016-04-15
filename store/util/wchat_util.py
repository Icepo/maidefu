# coding=utf-8

# 定义微信公众号参数
import json
import urllib2

app_id = 'wx34b1dc4a2245cd51'
app_secret = '1d9fb6d5e2d6e949cf708f679b8e2aac'
get_access_token = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + app_id + '&secret=' + app_secret
access_token = json.loads(urllib2.urlopen(get_access_token).read()).get('access_token')
print access_token
get_menu_api = 'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=' + access_token
print get_menu_api
current_menu = json.loads(urllib2.urlopen(get_menu_api).read())
print current_menu
new_menu = {u'url': u'http://www.baidu.com', u'type': u'view', u'name': u'测试页面'}
current_menu.get('selfmenu_info').get('button')[2].get('sub_button').get('list').append(new_menu)
current_menu_str = str(current_menu)
current_menu_str_encode = current_menu_str.encode("utf-8")
json = json.dumps(current_menu_str_encode).encode("utf-8")
print json, type(json)
set_menu = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + access_token
# print json.loads(urllib2.urlopen(set_menu, json.dumps(current_menu)).read())
