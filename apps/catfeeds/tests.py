# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Cats
from tagging.models import Tag, TaggedItem
from buffet import like_cat, recommend_cat, get_cats_by_tags, add_tags_cat, get_hot_tags, get_tags_cat
from buffet import  get_related_tags, add_tags_cat
from utils import get_cat_info_by_num_iid

class SimpleTest(TestCase):
    fixtures = ['catfeeds.json']
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
    def test_tags(self):
        cat = Cats.objects.create(num_iid=10, title='神州笔记本', cid=100000, price=1900, seller_credit_score=8)
        Tag.objects.update_tags(cat, '便宜 平民')
        cat = Cats.objects.create(num_iid=11, title='清华笔记本', cid=100000, price=1900, seller_credit_score=8)
        Tag.objects.update_tags(cat, '智慧  便宜')
        #print Tag.objects.get_for_object(cat)
        #cat = Cats.objects.get(num_iid = 10)
        #print cat.tags
        #cat.tags = '便宜, 平民'
        #print cat.tags
        
        #print Cats.tags.all()
        #print Cats.tags.related(['便宜'])
              
        
        '''
        tag = Tag.objects.get(name = "智慧 ")
        items = TaggedItem.objects.get_by_model(Cats, tag)
        for item in items:
            print item.title
        '''
        
    def test_buffet(self):
        like_cat(1, 10)
        recommend_cat(1);
        add_tags_cat(1, "便宜")
        print "#################"
        print get_cats_by_tags("便宜")[0].title
        print "#################"
        print get_tags_cat(1)
        add_tags_cat(1, "实惠")
        print "#################"
        print get_related_tags("便宜")
        print "#################"
        print get_hot_tags()
        
    def test_utils(self):
        get_cat_info_by_num_iid(1500008769583)
