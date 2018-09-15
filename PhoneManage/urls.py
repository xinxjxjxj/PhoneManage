#coding=utf-8
"""PhoneManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
#from Phone.views import index
#from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from Phone import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.index, name='login'),
    url(r'^accounts/login/$', views.index),
    url(r'login_action/', views.login_action),
    url(r'^home/$', views.home, name='home'),
    url(r'^homeborrow/$', views.homeborrow, name='homeborrow'),
    url(r'^Android_list/', views.Android_list, name="Android_list"),
    url(r'^Android_manage/', views.Android_manage, name="Android_manage"),
#     url(r'^search_name/$', views.search_name, name='Androidsearch'),
    url(r'^search/$', views.search, name='search'),
    url(r'^logout/$', views.logout),
    url(r'^iOS_list/', views.iOS_list, name="iOS_list"),
    url(r'^iOS_manage/', views.iOS_manage, name="iOS_manage"),
#     url(r'^search_name1/$', views.search_name1, name='iOSsearch'),
#     url(r'^search/$', views.search, name='iOSsearch'),
    url(r'^borrow/$', views.borrow, name='borrow'),
    url(r'^back/$', views.back, name='back'),
    url(r'^history_list/', views.history_list, name="history_list"),
    url(r'^applying/$', views.apply_list, name='applying'),
    url(r'^applycancel/$', views.apply_cancel, name='applied'),
    url(r'^reject/$', views.reject, name='reject'),
    url(r'^breakdown/$', views.breakdown, name='breakdown'),
    url(r'^repair/$', views.repair, name='repair'),
#     url(r'^historysearch/$', views.historysearch, name='historysearch'),
#     url(r'^search/$', views.search, name='historysearch'),
    url(r'^export/$', views.export, name='export'),
    url(r'^$', views.index, name='index'),
   
    #三个都要改
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

# handler404 = views.page_not_found
# handler500 = views.page_error
