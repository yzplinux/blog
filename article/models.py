from django.db import models
from django.contrib.auth.models import User
#时间
from django.utils import timezone
#标签
from taggit.managers import TaggableManager
#处理图片
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
#富文本编辑器
from ckeditor.fields import RichTextField
#mdeditor编辑器
from mdeditor.fields import MDTextField

# Create your models here.
class ArticleColumn(models.Model):
    title = models.CharField(max_length=10, blank=True,verbose_name='标题',unique=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=1)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100,unique=True)

    tags = TaggableManager(blank=True)

    description = models.CharField(max_length=100,blank=True)

    likes = models.PositiveIntegerField(default=0)

    avatar = ProcessedImageField(
        upload_to='article/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality': 100},
        blank=True
    )

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章正文。
    body = MDTextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    total_views = models.PositiveIntegerField(default=0)

    class Meta:
    # ordering 指定模型返回的数据的排列顺序
    # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    def increase_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])

    def increase_likes(self):
        self.likes += 1
        self.save(update_fields=['likes'])
