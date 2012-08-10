# -*- coding: utf-8 -*-

import json

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import top
import top.config as topconfig
import top.api as topapi

from models import Cats

def index(request):
    current_page = int(request.GET.get('page', '1'))
    pre_page,n_page,nn_page,nnn_page = 0,0,0,0
    if current_page > 1:
        pre_page = current_page - 1
    if current_page < 96:
        n_page = current_page + 1
        nn_page = current_page + 2
        nnn_page = current_page + 3
    
    search_key_word = request.GET.get('search_key_word', None)
    resp = []
    if search_key_word:
        req = topapi.TaobaokeItemsGetRequest(topconfig.URL, topconfig.PORT)
        req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
        
        req.fields="num_iid,title,nick,pic_url,price,\
                    click_url,commission,commission_rate,commission_num,\
                    commission_volume,shop_click_url,seller_credit_score,item_location,volume"
        req.pid = topconfig.PID
        req.keyword = search_key_word
        req.page_no = current_page
        
        #默认按照信用排序
        req.sort = ' credit_desc'
        try:
            resp = req.getResponse()['taobaoke_items_get_response']['taobaoke_items']['taobaoke_item']
            #print resp
        except Exception,e:
            print(e)
        
    #获取商品iid名称、图片、价格、佣金、佣金比例、商家地址、商品链接
    #num_iid, title, pic_url, price, commission, commission_rate, item_location, click_url
    return render_to_response('catfeeds/admin.html', 
                              {'itemlist':resp,
                               'current_page':current_page, 'pre_page':pre_page, 'n_page':n_page, 
                               'nn_page':nn_page, 'nnn_page':nnn_page, 'search_key_word':search_key_word})

def shopping(request):
    #获取商品id
    num_iid = request.GET.get('num_iid')
    
    #获取商品详细信息，并存入到数据库中
    req = topapi.TaobaokeItemsDetailGetRequest(topconfig.URL, topconfig.PORT)
    req.set_app_info(top.appinfo(topconfig.APPKEY, topconfig.APP_SECRECT))
    
    req.fields = 'desc,click_url,shop_click_url,seller_credit_score,num_iid,cid,\
                    title,nick,pic_url,price,desc'
    req.pid = topconfig.PID
    req.num_iids = num_iid
    try:
        #存入数据库
        resp = req.getResponse()
        #print resp
        item_detail = resp['taobaoke_items_detail_get_response']['taobaoke_item_details']['taobaoke_item_detail'][0]
        print item_detail
        cat = Cats(num_iid = item_detail['item']['num_iid'], cid = item_detail['item']['cid'],
                   title = item_detail['item']['title'], img_url = item_detail['item']['pic_url'],
                   click_url = item_detail['click_url'], price = item_detail['item']['price'],
                   seller_credit_score = item_detail['seller_credit_score'], desc = item_detail['item']['desc'])
        cat.save()
    except Exception,e:
        print(e)
        return HttpResponse('Err:' + str(e))
        
    return HttpResponse(str('OK，成功加入数据库'))