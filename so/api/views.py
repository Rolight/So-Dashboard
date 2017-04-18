from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

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
        data = sl.WebsiteAllowedDomainSerializer(self.queryset, many=True).data
        return Response(data=data)


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
        data = request.data
        pattern_type = data.get('type', 0)
        self.queryset = WebsiteUrlPattern.objects.filter(
            website_id=website_pk,
            pattern_type=pattern_type
        )
        data = sl.WebsiteUrlPatternSerializer(self.queryset, many=True).data
        return Response(data=data)


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
        data = sl.WebsiteSelectorSerializer(self.queryset, many=True).data
        return Response(data=data)


class WebsiteSelectorViewSet(ModelViewSet):
    serializer_class = sl.WebsiteSelectorSerializer
    queryset = WebsiteSelector.objects.all()
    rest_actions = ('retrieve', 'update', 'destroy')
