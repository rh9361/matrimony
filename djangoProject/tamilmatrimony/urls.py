# from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from tamilmatrimony import views

urlpatterns = [

    path('', views.profile_list, name='list'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('shownInterest/', views.shownInterest, name='shownInterest'),
    path('thankyou/', views.thankyou, name='thankyou'),

    path('search/', views.profile_search_list, name='search1'),
    path('search_by_id/', views.profile_search_id, name='search2'),

    path('create/', views.profile_create, name='create'),
    path('myprofile/', views.my_profile, name='myprofile'),
    path('all_profiles/', views.profile_list_all, name='allprofiles'),

    path('myprofile/edit/', views.myprofile_update, name='myedit'),

    url('(?P<slug>[\w.@+-]+)/', views.profile_detail, name='details'),
    url('(?P<slug>[\w.@+-]+)/edit/', views.profile_update, name='edit'),

    url('(?P<slug>[\w.@+-]+)/delete/', views.profile_delete),

]

app_name = 'tamilmatrimony'
