from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView,DetailView,DeleteView,View,FormView
from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import ArticlePost,ArticleColumn
from .forms import ArticlePostForm


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
        context['columns'] = ArticleColumn.objects.all()
        return self.render_to_response(context)


class ArticleCreateView(CreateView):
    model = ArticlePost
    fields = ['title','body','description']
    template_name = 'article/create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(form=ArticlePostForm)
        return (context)
