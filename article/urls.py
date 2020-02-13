#!/usr/bin/env python 
# -*- coding:utf-8 -
from django.urls import path
from . import views
app_name = 'article'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('create/',views.ArticleCreateView.as_view(),name='article_create'),
    #path('create/', views.articlecreate, name='article_create'),

]