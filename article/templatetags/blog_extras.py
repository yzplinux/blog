#!/usr/bin/env python 
# -*- coding:utf-8 -
from django import template
from ..models import ArticlePost

register = template.Library()


@register.inclusion_tag('inclusions/_hot_articles.html', takes_context=True)
def show_hot_articles(context, num=8):
    return {
        'hot_article_list': ArticlePost.objects.all().order_by('-total_views')[:num],
    }