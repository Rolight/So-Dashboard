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
from django.conf.urls import url, include
from rest_framework_nested import routers
from rest_framework_jwt.views import (
    obtain_jwt_token, verify_jwt_token
)

from so.api import views

router = routers.SimpleRouter()
router.register(r'websites', views.WebsiteViewSet)
router.register(r'websitealloweddomains', views.WebsiteAllowedDomainViewSet)
router.register(r'websiteurlpatterns', views.WebsiteUrlPatternViewSet)
router.register(r'websiteselectors', views.WebsiteSelectorViewSet)
router.register(r'spidertasks', views.SpiderTaskViewSet)

website_parent_router = routers.NestedSimpleRouter(
    router, r'websites', lookup='website')

website_parent_router.register(
    r'websitealloweddomains',
    views.WebsiteAllowedDomainNestedViewSet,
    base_name='websitealloweddomains'
)
website_parent_router.register(
    r'websiteurlpatterns',
    views.WebsiteUrlPatternNestedViewSet,
    base_name='websiteurlpatterns'
)
website_parent_router.register(
    r'websiteselectors',
    views.WebsiteSelectorNestedViewSet,
    base_name='websiteselectors'
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(website_parent_router.urls)),
    url(r'^login/$', obtain_jwt_token),
    url(r'^user/$', verify_jwt_token),
    url(r'^search/$', views.SearchView.as_view()),
]
