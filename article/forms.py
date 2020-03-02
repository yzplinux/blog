#!/usr/bin/env python 
# -*- coding:utf-8 -
from django import forms
from .models import ArticlePost

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title','body','description','column','tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #自定义
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'文章标题',
            'id':'text',
            'required':True,
            })
        self.fields['tags'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'文章标签',
            'id':'tags',
            'name':'tags',
            'required':True
            })

        #通用
        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'col-9'})
