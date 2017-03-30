from rest_framework.viewsets import ModelViewSet

from so.models import (
    Website,
    WebsiteAllowedDomain,
    WebsiteUrlPattern,
    WebsiteSelector
)
from so import serializers as sl


class WebsiteViewSet(ModelViewSet):
    serializer_class = sl.WebsiteSerialzer
    queryset = Website.objects.all()
    rest_actions = ('create', 'update', 'list', 'retrieve', 'destroy')


class WebsiteAllowedDomainNestedViewSet(ModelViewSet):
    serializer_class = sl.WebsiteAllowedDomainSerializer
    queryset = WebsiteAllowedDomain.objects.all()
    rest_actions = ('list', 'create')

    def create(self, request, website_pk):
        request.data['website_id'] = website_pk
        return super().create(request)

    def list(self, request, website_pk):
        self.queryset = WebsiteAllowedDomain.objects.filter(
            website_id=website_pk)
        return super().list(request)


class WebsiteAllowedDomainViewSet(ModelViewSet):
    serializer_class = sl.WebsiteAllowedDomainSerializer
    queryset = WebsiteAllowedDomain.objects.all()
    rest_actions = ('retrieve', 'update', 'destroy')


class WebsiteUrlPatternNestedViewSet(ModelViewSet):
    serializer_class = sl.WebsiteUrlPatternSerializer
    queryset = WebsiteUrlPattern.objects.all()
    rest_actions = ('list', 'create')

    def create(self, request, website_pk):
        request.data['website_id'] = website_pk
        return super().create(request)

    def list(self, request, website_pk):
        self.queryset = WebsiteUrlPattern.objects.filter(
            website_id=website_pk)
        return super().list(request)


class WebsiteUrlPatternViewSet(ModelViewSet):
    serializer_class = sl.WebsiteUrlPatternSerializer
    queryset = WebsiteUrlPattern.objects.all()
    rest_actions = ('retrieve', 'update', 'destroy')


class WebsiteSelectorNestedViewSet(ModelViewSet):
    serializer_class = sl.WebsiteSelectorSerializer
    queryset = WebsiteSelector.objects.all()
    rest_actions = ('list', 'create')

    def create(self, request, website_pk):
        request.data['website_id'] = website_pk
        return super().create(request)

    def list(self, request, website_pk):
        self.queryset = WebsiteSelector.objects.filter(
            website_id=website_pk)
        return super().list(request)


class WebsiteSelectorViewSet(ModelViewSet):
    serializer_class = sl.WebsiteSelectorSerializer
    queryset = WebsiteSelector.objects.all()
    rest_actions = ('retrieve', 'update', 'destroy')
