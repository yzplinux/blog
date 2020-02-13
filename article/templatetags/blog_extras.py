#!/usr/bin/env python 
# -*- coding:utf-8 -
from django import template
from ..models import ArticlePost

register = template.Library()


@register.inclusion_tag('inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': ArticlePost.objects.all().order_by('-created')[:num],
    }