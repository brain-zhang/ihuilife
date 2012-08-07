# -*- coding: utf-8 -*-

import json

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import top
import top.config as topconfig
import top.api as topapi

def index(request):
    req = topapi.TaobaokeItemsGetRequest(topconfig.URL, topconfig.PORT)
    req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
    #req.set_app_info(top.appinfo('1021098591','sandbox5f068ad98a7d39f148ea9a25e'))
    
    req.fields="num_iid,title,nick,pic_url,price,\
                click_url,commission,commission_rate,commission_num,\
                commission_volume,shop_click_url,seller_credit_score,item_location,volume"
    req.pid = topconfig.PID
    req.keyword = "生活小工具"
    try:
        resp = req.getResponse()
        print resp
    except Exception,e:
        print(e)
        
    #获取商品iid名称、图片、价格、佣金、佣金比例、商家地址、商品链接
    #num_iid, title, pic_url, price, commission, commission_rate, location, click_url
    
    #resp = json.loads(resp)
    #print resp
    return render_to_response('catfeeds/admin.html')

