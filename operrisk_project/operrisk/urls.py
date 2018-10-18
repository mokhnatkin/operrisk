from django.urls import path
from django.conf.urls import url
from operrisk import views
from django.shortcuts import render

urlpatterns = [    
    path('', views.index, name='index'),
    url(r'^category/(?P<category_URL_name>[\w\-]+)/$',views.show_category,name='show_category'),
    url(r'^incidents/(?P<incident_id>[\w\-]+)/$',views.show_incident,name='show_incident'),
    path('all_incidents/', views.show_all_incidents, name='all_incidents'),
    path('add_incident/',views.add_incident,name="add_incident")
]