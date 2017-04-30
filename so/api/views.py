from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny

from so.models import (
    Website,
    WebsiteAllowedDomain,
    WebsiteUrlPattern,
    WebsiteSelector,
    SpiderTask
)
from so import serializers as sl
from so import core
from so.constant import constant


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
        data = request.query_params
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
        data = request.query_params
        pattern_type = int(data.get('type', 2))
        if pattern_type == 0:
            self.queryset = self.queryset.filter(key_name='title')
        elif pattern_type == 1:
            self.queryset = self.queryset.filter(key_name='body')
        elif pattern_type == 2:
            self.queryset = self.queryset.exclude(
                key_name__in=['title', 'body']
            )
        data = sl.WebsiteSelectorSerializer(self.queryset, many=True).data
        return Response(data=data)


class WebsiteSelectorViewSet(ModelViewSet):
    serializer_class = sl.WebsiteSelectorSerializer
    queryset = WebsiteSelector.objects.all()
    rest_actions = ('retrieve', 'update', 'destroy')


class SpiderTaskViewSet(ModelViewSet):
    serializer_class = sl.WebsiteSerialzer
    queryset = Website.objects.all()
    rest_actions = ('list', 'update', 'destory', 'retrieve')
    permission_classes = (AllowAny, )

    @list_route(methods=['get'], url_path='spiders')
    def list_spiders(self, request):
        spider_data = core.get_spiders()
        return Response(data=spider_data)

    def list(self, request):
        data = request.query_params
        spider = data.get('spider')
        if not spider:
            return Response()
        tasks = SpiderTask.objects.filter(spider=spider).order_by(
            '-id')[:10]
        data = sl.SpiderTaskSerializer(tasks, many=True).data
        return Response(data=data)

    @list_route(methods=['delete'], url_path='clear')
    def stop_spider_tasks(self, request):
        data = request.query_params
        spider = data.get('spider')
        if not spider:
            return Response()
        core.stop_spider_task(spider)
        return Response()

    @detail_route(methods=['put'], url_path='sync')
    def sync_log(self, request, pk):
        data = request.data
        spider = data.get('spider')
        if not spider:
            return Response()
        core.fetch_log(pk, spider)
        return Response()

    @detail_route(methods=['get'], url_path='log')
    def get_log(self, request, pk):
        try:
            spider_task = SpiderTask.objects.get(pk=pk)
        except SpiderTask.DoesNotExist:
            return Response()

        data = request.query_params
        line = int(data.get('line', 0))

        log_lines = spider_task.logs.split('\n')
        return Response(data=log_lines[line:])

    def update(self, request, pk):
        spider_task = SpiderTask.objects.get(pk=pk)
        spider_task.status = constant.FINISH
        spider_task.save()
        return Response()
