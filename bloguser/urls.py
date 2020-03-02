#!/usr/bin/env python 
# -*- coding:utf-8 -
from django.contrib import admin
from django.urls import path
from . import views

app_name='bloguser'

urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.user_logout,name='logout')
]

