from django.urls import path
from django.conf.urls import url
from operrisk import views
from django.shortcuts import render

urlpatterns = [    
    path('', views.index, name='index'),
    url(r'^category/(?P<category_URL_name>[\w\-]+)/$',views.show_category,name='show_category'),#show all incidents in the category
    url(r'^incidents/(?P<incident_id>[\w\-]+)/$',views.show_incident,name='show_incident'),#show info about incident
    path('all_incidents/', views.show_all_incidents, name='all_incidents'),#list of incidents
    path('all_incidents_f/', views.show_all_incidents_f, name='all_incidents_f'),#list of incidents w/ filter
    path('all_incidents_p/', views.show_all_incidents_p, name='all_incidents_p'),#list of incidents w/ pagination
    path('add_incident/',views.add_incident,name="add_incident"),#add a new incident    
    path('export_incidents/',views.export_incidents,name="export_incidents"),#exports incidents to excel file
    path('list_users/',views.list_users,name="list_users"),#list of all users of APP    
]