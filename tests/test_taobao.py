# -*- coding: utf-8 -*-
import top.api as topapi
import top

url = 'gw.api.taobao.com'
port = 80
appkey = '21098591'
secret = '7e440955f068ad98a7d39f148ea9a25e'
PID = 32399943

req=topapi.TaobaokeCaturlGetRequest(url,port)
req.set_app_info(top.appinfo(appkey,secret))

req.cid=1
req.nick="memorybox"
try:
    resp= req.getResponse()
    print(resp)
except Exception,e:
    print(e)
