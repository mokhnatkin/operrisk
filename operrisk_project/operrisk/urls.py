from django.urls import path
from django.conf.urls import url
from operrisk import views
from django.shortcuts import render

urlpatterns = [    
    path('', views.index, name='index'),
    path('category/<str:category_URL_name>', views.show_category, name='show_category'),#show all incidents in the category
    path('subcategory/<str:subcategory_URL_name>', views.show_subcategory, name='show_subcategory'),#show all incidents in the subcategory
    path('incidents/<int:id>/', views.show_incident, name='show_incident'),#show info about incident
    path('my_incidents/', views.show_my_incidents, name='my_incidents'),#list of incidents added by current user
    path('all_incidents_f/', views.show_all_incidents_f, name='all_incidents_f'),#list of incidents w/ filter
    path('all_incidents_p/', views.show_all_incidents_p, name='all_incidents_p'),#list of incidents w/ pagination
    path('add_incident/',views.edit_incident,name="add_incident"),#add a new incident
    path('edit_incident/<int:id>/', views.edit_incident, {}, name='edit_incident'),#edit the incident
    path('approve_incident/<int:id>/', views.approve_incident, {}, name='approve_incident'),#approve the incident
    path('cancel_incident/<int:id>/', views.cancel_incident, {}, name='cancel_incident'),#cancel the incident
    path('export_incidents/',views.export_incidents,name="export_incidents"),#exports incidents to excel file
    path('list_users/',views.list_users,name="list_users"),#list of users
]