from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def home_page_view(request):
    return render(request, 'so/home.html')
