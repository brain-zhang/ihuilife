# -*- coding: utf-8 -*-

import json

from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import top
import top.config as topconfig
import top.api as topapi

from ihuilife.apps.catfeeds.buffet import get_hot_tags, get_hot_cats

def index(request):
    hottags = get_hot_tags()
    hotcats = get_hot_cats(8)
    return render_to_response('index.html', {'hottags':hottags, 'hotcats':hotcats})