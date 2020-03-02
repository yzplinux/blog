#!/usr/bin/env python 
# -*- coding:utf-8 -
from django.urls import path
from . import views
app_name = 'article'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('create/',views.ArticleCreateView.as_view(),name='article_create'),
    path('detail/<int:pk>',views.ArticleDetailView.as_view(),name='article_detail'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),
]