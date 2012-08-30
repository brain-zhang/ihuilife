# -*- coding: utf-8 -*-

import json

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import top
import top.config as topconfig
import top.api as topapi

from models import Cats
from buffet import recommend_cat
from utils import get_taobaoke_cat_info_by_num_iid, get_cat_info_by_num_iid

def search_index(request):
    '''
    根据关键字搜索淘宝客商品，前台页面
    '''
    current_page = int(request.GET.get('page', '1'))
    pre_page, n_page, nn_page, nnn_page = 0, 0, 0, 0
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
        
        req.fields = "num_iid,title,nick,pic_url,price,\
                    click_url,commission,commission_rate,commission_num,\
                    commission_volume,shop_click_url,seller_credit_score,item_location,volume"
        req.pid = topconfig.PID
        req.keyword = search_key_word
        req.page_no = current_page
        
        #默认按照信用排序
        req.sort = 'credit_desc'
        try:
            resp = req.getResponse()['taobaoke_items_get_response']['taobaoke_items']['taobaoke_item']
            #print resp
        except Exception, e:
            print(e)
        
    #获取商品iid名称、图片、价格、佣金、佣金比例、商家地址、商品链接
    #num_iid, title, pic_url, price, commission, commission_rate, item_location, click_url
    return render_to_response('catfeeds/search.html',
                              {'itemlist':resp,
                               'current_page':current_page, 'pre_page':pre_page, 'n_page':n_page,
                               'nn_page':nn_page, 'nnn_page':nnn_page, 'search_key_word':search_key_word})

def num_iid_index(request):
    '''
    根据商品num_iid入库，前台页面
    '''
    return render_to_response('catfeeds/taobao.html')

def taobaoke_shopping(request):
    '''
    获取商品id(针对淘宝客商品)
    '''
    num_iid = request.GET.get('num_iid')
    
    try:
        get_taobaoke_cat_info_by_num_iid(num_iid)
    except Exception, e:
        print(e)
        return HttpResponse('Err:' + str(e))
        
    return HttpResponse(str('OK，成功加入数据库'))

def taobao_shopping(request):
    '''
    根据商品id写入数据库(针对普通商品)
    '''
    num_iid = request.GET.get('num_iid')
    
    try:
        get_cat_info_by_num_iid(num_iid)
    except Exception, e:
        print(e)
        return HttpResponse('Err:' + str(e))
        
    return HttpResponse(str('OK，成功加入数据库'))

def recommendcat(request):
    '''
    管理员推荐一个商品，默认此商品评分+10
    '''
    try:
        num_iid = request.GET.get('num_iid')
        recommend_cat(num_iid)
    except Exception, e:
        print(e)
        return HttpResponse('Err:' + str(e))
    return HttpResponse(str('OK，成功')) 
