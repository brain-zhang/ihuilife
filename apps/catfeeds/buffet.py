# -*- coding: utf-8 -*-
from tagging.models import Tag, TaggedItem
from models import Cats

def like_cat(cat_id, fan_id):
    '''
    用户喜欢一个商品
    '''
    #首先取出商品当前的fans
    item = Cats.objects.get(num_iid = cat_id)
    fan_ids = list(item.fans)
    if not fan_id in fan_ids:
        fan_ids.append(fan_id)
    item.fans = str(fan_ids)
    
    #更新数据库
    item.save()
        
def recommend_cat(cat_id):
    '''
    站长推荐一个商品
    '''
    item = Cats.objects.get(num_iid = 1)
    item.rating += 10
    item.save()
    
def get_recommend_cats():
    '''
    获取推荐物品
    '''

def add_tags_cat(cat_id, tag_name):
    '''
    为一个商品添加tag
    '''
    item = Cats.objects.get(num_iid = cat_id)
    Tag.objects.add_tag(item, tag_name)

def get_tags_cat(cat_id):
    '''
    获取一个商品的tag
    '''    
    item = Cats.objects.get(num_iid = cat_id)
    return item.tags

def get_hot_tags():
    '''
    获取当前的热门标签
    '''
    tags = Tag.objects.usage_for_model(Cats, counts = True)
    hottags = [(tag.name, tag.count) for tag in tags]
    
    #sort by count
    sorted(hottags, key = lambda hottag:hottag[1])
    return [hottag[0] for hottag in hottags]

def get_cats_by_tags(tag_names):
    '''
    获取此标签对应的商品
    '''
    tag_names = tag_names.split(' ')
    tag = [Tag.objects.get(name = tag_name) for tag_name in tag_names]
    return TaggedItem.objects.get_by_model(Cats, tag)

def get_related_tags(tag_name):
    '''
    获取与此标签类似的标签
    '''
    return Cats.tags.related(tag_name.split(' '))

def get_hot_cats(limit = 20):
    '''
    获取评分高的商品
    '''
    return Cats.objects.order_by('-rating')[0:limit]