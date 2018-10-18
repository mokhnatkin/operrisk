from django.urls import path
from django.conf.urls import url
from operrisk import views
from django.shortcuts import render

urlpatterns = [    
    path('', views.index, name='index'),
    url(r'^category/(?P<category_URL_name>[\w\-]+)/$',views.show_category,name='show_category')
]