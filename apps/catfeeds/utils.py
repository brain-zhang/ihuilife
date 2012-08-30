# -*- coding: utf-8 -*-
#全量获取后台类目，每天自动更新
import time

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import top
import top.config as topconfig
import top.api as topapi

from models import ItemCats, Cats

def get_taobaoke_cat_info_by_num_iid(num_iid):    
    '''
    获取淘宝客商品详细信息，并存入到数据库中
    '''
    req = topapi.TaobaokeItemsDetailGetRequest(topconfig.URL, topconfig.PORT)
    req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
    
    req.fields = 'desc,click_url,shop_click_url,seller_credit_score,num_iid,cid,\
                    title,nick,pic_url,price,desc,item_imgs'
    req.pid = topconfig.PID
    req.num_iids = num_iid
    
    #存入数据库
    resp = req.getResponse()
    #print resp
    item_detail = resp['taobaoke_items_detail_get_response']['taobaoke_item_details']['taobaoke_item_detail'][0]
    print item_detail
    cat = Cats(num_iid=item_detail['item']['num_iid'], cid=item_detail['item']['cid'],
               title=item_detail['item']['title'], img_url=item_detail['item']['pic_url'],
               click_url=item_detail['click_url'], price=item_detail['item']['price'],
               seller_credit_score=item_detail['seller_credit_score'], desc=item_detail['item']['desc'],
               item_imgs=item_detail['item']['item_imgs'], is_taobaoke=True)
    cat.save()

        
def get_cat_info_by_num_iid(num_iid):
    '''
    根据链接地址获取商品信息，存到数据库中
    '''      
    req = topapi.ItemGetRequest(topconfig.URL, topconfig.PORT)
    req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
    
    req.fields = "detail_url,num_iid,title,cid,desc,pic_url,price,item_imgs"
    req.num_iid = num_iid
           
    resp = req.getResponse()
    item_detail = resp['item_get_response']['item']
    cat = Cats(num_iid=item_detail['num_iid'], cid=item_detail['cid'],
               title=item_detail['title'], img_url=item_detail['pic_url'],
               click_url=item_detail['detail_url'], price=item_detail['price'],
               item_imgs=item_detail['item_imgs'], desc=item_detail['desc'], is_taobaoke=False,
        #这里默认还有一个字段，获取卖家信用，但是在沙盒中无法测试此参数的有效性，暂时不填上
        seller_credit_score = item_detail.get('score', -1))
    print item_detail
    cat.save()
        
def get_itemcats(request):
    '''
    获取商品类目，构建列表到数据库中
    '''
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
            itemcats = ItemCats(cid=item['cid'], name=item['name'], parent_cid=item['parent_cid'])   
            itemcats.save()     
        except:
            pass
        
def _get_cat_cid_info(cid, is_parent_cid):
    time.sleep(1)
    
    req = topapi.ItemcatsGetRequest(topconfig.URL, topconfig.PORT)
    req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
    
    req.fields = 'cid,parent_cid,name,is_parent'
    if is_parent_cid:
        req.parent_cid = cid
    else:
        req.cids = cid
    try:
        resp = req.getResponse()
        return resp['itemcats_get_response']['item_cats']['item_cat']
    except Exception, e:
        print(e)
        return None
    
if __name__ == '__main__':
    get_itemcats(None)
