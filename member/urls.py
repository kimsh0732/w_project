# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:30:39 2022

@author: KITCOOP
member 폴더
urls.py
"""
from django.urls import path
from . import views
# http://localhost:8000/member
urlpatterns = [
    #http://localhost:8000/member/login 요청시 => views.py의 login 메서드 호출
    path('login/',views.login,name='login'),

    #http://localhost:8000/member/join 요청시 => views.py의 join 메서드 호출
    path('join/', views.join,name='join'),
    path('main/', views.main,name='main'),
    path('logout/', views.logout,name='logout'),
    path('info/<str:id>/', views.info,name='info'),  # /member/info/admin/ => 형태
    path('update/<str:id>/', views.update, name='update'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('password/<str:id>/', views.password, name='password'),
    path('list/', views.list,name='list'),    
    path('picture/', views.picture,name='picture'),    
]
