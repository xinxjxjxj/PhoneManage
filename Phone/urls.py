#coding=utf-8
'''
Created on 2017年6月16日

@author: xinjian
'''
from django.conf.urls import url
from views import *
#from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^login/$', index, name='login'),
    url(r'^accounts/login/$', index),
    url(r'login_action/', login_action),
    url(r'^Android_list/', Android_list, name="Android_list"),
    url(r'^Android_manage/', Android_manage, name="Android_manage"),
    url(r'^search_name/$', search_name, name='Androidsearch'),
    url(r'^logout/$', logout),
    url(r'^iOS_list/', iOS_list, name="iOS_list"),
    url(r'^iOS_manage/', iOS_manage, name="iOS_manage"),
    url(r'^search_name1/$', search_name1, name='iOSsearch'),
    url(r'^borrow/$', borrow, name='borrow'),
    url(r'^back/$', back, name='back'),
    url(r'^history_list/', history_list, name="history_list"),
    url(r'^applying/$', apply_list, name='applying'),
    url(r'^applycancel/$', apply_cancel, name='applied'),
    url(r'^reject/$', reject, name='reject'),
    url(r'^breakdown/$', breakdown, name='breakdown'),
    url(r'^repair/$', repair, name='repair'),
    url(r'^historysearch/$', historysearch, name='historysearch'),
    url(r'^export/$', export, name='export'),
    url(r'', Android_list, name="Android_list"),
   
    #三个都要改
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

handler404 = page_not_found
handler500 = page_error

