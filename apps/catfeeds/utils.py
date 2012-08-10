# -*- coding: utf-8 -*-
#全量获取后台类目，每天自动更新
import time

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import top
import top.config as topconfig
import top.api as topapi

from models import ItemCats

def get_itemcats(request):
    #获取所有商品类目，构建列表到数据库中
    item_cats_list = _get_cat_cid_info(0, True)
    _get_itemcats_list(item_cats_list)
    return HttpResponse('OK')
        
def _get_itemcats_list(cats_list):    
    if not cats_list:
        return    
    item_parent_lists = [item for item in cats_list if item['is_parent']]
    
    _set_itemcats_db(cats_list)
    
    for item in item_parent_lists:
        _get_itemcats_list(_get_cat_cid_info(item['cid'], item['is_parent']))
    
def _set_itemcats_db(cats_list):
    for item in cats_list:
        try:
            itemcats = ItemCats(cid = item['cid'], name = item['name'], parent_cid = item['parent_cid'])   
            itemcats.save()     
        except:
            pass
        
def _get_cat_cid_info(cid, is_parent_cid):
    time.sleep(1)
    
    req = topapi.ItemcatsGetRequest(topconfig.URL, topconfig.PORT)
    req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
    
    req.fields='cid,parent_cid,name,is_parent'
    if is_parent_cid:
        req.parent_cid = cid
    else:
        req.cids = cid
    try:
        resp= req.getResponse()
        return resp['itemcats_get_response']['item_cats']['item_cat']
    except Exception,e:
        print(e)
        return None
    
if __name__ == '__main__':
    get_itemcats(None)