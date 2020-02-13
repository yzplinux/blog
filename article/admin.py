from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ArticleColumn
from .models import ArticlePost
from mdeditor.widgets import MDEditorWidget
from django.db import models


class ArticlePostlAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }

# 注册ArticlePost到admin中
admin.site.register(ArticlePost, ArticlePostlAdmin)
admin.site.register(ArticleColumn)
