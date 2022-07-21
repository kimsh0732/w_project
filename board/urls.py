# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 09:30:03 2022

@author: KITCOOP
board/urls.py
  http://localhost:8000/board/xxxxx 요청시 호출
"""
from django.urls import path
from . import views
urlpatterns = [
    path('list/',views.list,name='list'),
    path('write/', views.write,name='write'),
    path('info/<int:num>/', views.info,name='info'),
    path('update/<int:num>/', views.update,name='update'),
    path('delete/<int:num>/', views.delete,name='delete'),
    
]    