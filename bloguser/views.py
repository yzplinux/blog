from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .forms import UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView,DetailView,UpdateView,ListView,View
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

class UserLoginView(FormView):
    template_name = 'bloguser/login.html'
    form_class = UserLoginForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect(self.success_url)
            else:
                messages.error(request, '账号或密码输入有误。请重新输入!')
                return redirect('.')
        else:
            return HttpResponse('表单输入有误！')



def user_logout(request):
    logout(request)
    return redirect('/')