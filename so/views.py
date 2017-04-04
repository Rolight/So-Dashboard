from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


@login_required
def home_page_view(request):
    return render(request, 'so/home.html')


def user_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid() and form.get_user():
            login(request, form.get_user())
            return redirect(reverse('home_page'))
    return render(request, 'so/login.html')


@login_required
def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('home_page'))
