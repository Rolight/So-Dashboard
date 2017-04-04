"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from so.views import (
    home_page_view,
    user_login_view,
    user_logout_view
)


urlpatterns = [
    url(r'^$', home_page_view, name='home_page'),
    url(r'^login/$', user_login_view, name='user_login'),
    url(r'^logout/$', user_logout_view, name='user_logout'),
]
