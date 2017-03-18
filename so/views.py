from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from so.forms import (
    RegisterForm, LoginForm, UserPassWordChangeForm
)


@login_required
def home_page(request):
    return render(request, 'home.html')


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid() and form.get_user():
            login(request, form.get_user())
            return redirect(reverse('home_page'))
    return render(request, 'so/form_template.html', context={
        'title': '用户登录',
        'form': form,
        'form_action': reverse('login'),
        'submit_text': '登录'
    })


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    return render(request, 'so/form_template.html', context={
        'title': '用户注册',
        'form': form,
        'form_action': reverse('register'),
        'submit_text': '注册'
    })


@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home_page'))


# 修改密码
@login_required
def change_password_view(request):
    context = {
        'title': '修改密码',
        'submit_text': '确认修改',
        'form_action': reverse('change_password')
    }
    form = UserPassWordChangeForm(request.user)
    if request.method == 'POST':
        form = UserPassWordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home_page'))
    context['form'] = form
    return render(request, 'so/form_template.html', context=context)
