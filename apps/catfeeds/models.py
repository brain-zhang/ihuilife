# -*- coding: utf-8 -*-
from django.db import models
import tagging

# Create your models here.
class Cats(models.Model):
    #商品唯一标识
    num_iid = models.IntegerField(unique=True)
    
    #商品名称
    title = models.CharField(max_length=512)
    
    #宣传图片
    img_url = models.CharField(max_length=256)
    
    #分类
    cid = models.IntegerField()
    
    #淘宝客链接
    click_url = models.CharField(max_length=256)
    
    #价格
    price = models.FloatField()
    
    #卖家信用
    seller_credit_score = models.IntegerField()
    
    #商品描述
    desc = models.CharField(max_length=1024)
    
    #评价
    rating = models.IntegerField(default=0)
    
    #喜欢这件商品的人，存储用户id
    fans = models.TextField()
    
    #是否是淘宝客推荐品
    is_taobaoke = models.BooleanField()
    
    #详细图片列表
    item_imgs = models.TextField()
    
tagging.register(Cats)
    
class ItemCats(models.Model):
    #分类
    cid = models.IntegerField(unique=True)
    
    #分类名称
    name = models.CharField(max_length=512)
    
    #父类名称
    parent_cid = models.IntegerField()
