from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView,DetailView,DeleteView,View,FormView
from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import ArticlePost,ArticleColumn
from .forms import ArticlePostForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import re
import markdown
# Create your views here.

class Home(ListView):
    model = ArticlePost
    template_name = 'home.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.order = request.GET.get('order')
        if self.order == 'total_views':
            self.ordering = '-total_views'
        self.search = request.GET.get('search')
        self.tag = request.GET.get('tag')
        self.column = request.GET.get('column')
        self.object_list = self.get_queryset()
        if self.tag and self.tag != None:
            context = self.get_context_data(object_list=self.object_list.filter(tags__name__in=[self.tag]))
            context['tag'] = self.tag
        else:
            context = self.get_context_data()
        if self.search:
            context = self.get_context_data(object_list=self.object_list.filter(
                Q(title__icontains=self.search) |
                Q(body__icontains=self.search)))
            context['search'] = self.search
        else:
            self.search = ''
        if self.column:
            context = self.get_context_data(object_list=self.object_list.filter(column_id=self.column))
            context['column'] = self.column
        context['columns'] = ArticleColumn.objects.all()
        return self.render_to_response(context)

class ArticleCreateView(CreateView):
    model = ArticlePost
    fields = ['title','body','description','column','tags']
    template_name = 'article/create.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            article = self.model.objects.filter(title=request.POST.get('title'))
            self.object = form.save()
            #first()：返回queryset中匹配到的第一个对象，如果没有匹配到对象则为None，如果queryset没有定义排序，则按主键自动排序。
            article_id = article.first().id
            return redirect('article:article_detail',pk=article_id)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(form=ArticlePostForm)
        context['columns'] = ArticleColumn.objects.all()
        return (context)

@method_decorator(login_required(login_url='/userprofile/login/'),name='dispatch')
class ArticleUpdateView(UpdateView):
    model = ArticlePost
    fields = ['title', 'body', 'description', 'column', 'tags']
    template_name = 'article/update.html'

    def get_success_url(self):
        return reverse_lazy('article:article_detail',kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data()
        context['tags'] = ','.join([x for x in self.object.tags.names()])
        context['columns'] = ArticleColumn.objects.all()
        context['title_len'] = len(context['object'].title)
        return context

class ArticleDetailView(DetailView):
    model = ArticlePost
    template_name = 'article/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        #需要先调用父类的方法才能有self.object
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        article = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        article.body = md.convert(article.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        article.toc = m.group(1) if m is not None else ''
        return article

class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.increase_likes()
        return HttpResponse('success')
