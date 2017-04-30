import json

from django.conf import settings
from elasticsearch import Elasticsearch

from so import cache_keys
from so.cache import redis_cache
from so.constant import constant
from so.models import (
    Website,
    WebsiteAllowedDomain,
    WebsiteUrlPattern,
    WebsiteSelector,
    SpiderTask,
)


test_data = {
    "website_id": 406,
    "task_id": 1,
    "index": "rolight-sample-1",
    "es_host": settings.ES_HOST,
    "allowed_domains": ["spidertest-app.smartgslb.com"],
    "start_urls": ["http://spidertest-app.smartgslb.com"],
    "sleep": 1,
    "parse_url_rules": [
        r"http://spidertest-app.smartgslb.com/\d{4}/\d{2}/\d{2}/.*",
    ],
}


def get_spiders():
    cluster_key = cache_keys.key_of_spider_cluster()
    all_spiders = [s.decode() for s in redis_cache.smembers(cluster_key)]
    spiders = []
    for spider in all_spiders:
        spider_key = cache_keys.key_of_spider(spider)
        spider_data = redis_cache.get(spider_key)
        if spider_data is not None:
            task_data = json.loads(spider_data.decode())
            website_id = task_data['website_id']
            try:
                website = Website.objects.get(pk=website_id)
                website = website.title
            except Website.DoesNotExist:
                website = ''
            task_data['website'] = website
            spiders.append(task_data)
    return {'all_spiders': all_spiders, 'spiders': spiders}


def stop_spider_task(spider):
    spider_key = cache_keys.key_of_spider(spider)
    spider_data = redis_cache.get(spider_key)
    if spider_data is None:
        return
    spider_data = json.loads(spider_data.decode())
    if spider_data['status'] == 'running':
        command_key = cache_keys.key_of_task_command(
            spider_data['task_id'],
            'stop'
        )
        redis_cache.incr(command_key)


def fetch_log(task_id, spider):
    try:
        spider_task = SpiderTask.objects.get(pk=task_id)
    except SpiderTask.DoesNotExist:
        return

    if spider_task.spider != spider:
        spider_task.spider = spider
        spider_task.save()

    log_key = cache_keys.key_of_task_log(task_id)
    log_len = redis_cache.llen(log_key)
    if log_len == 0:
        return
    log_data = []
    for _ in range(log_len):
        data = redis_cache.lpop(log_key)
        if data:
            log_data.append(data.decode())
    spider_task.logs += ''.join(log_data)
    spider_task.save()


def run_task(task):
    website_id = task['website_id']
    spider_task = SpiderTask.objects.create(website_id=website_id,)
    task['task_id'] = spider_task.pk
    task_data = json.dumps(task)
    task_queue_key = cache_keys.key_of_task_queue()
    redis_cache.rpush(task_queue_key, task_data)


def create_website_spider_task(website_id):
    website = Website.objects.get(pk=website_id)
    task = {
        'website_id': website.pk,
        'index': 'so-index-%d' % website_id,
        'es_host': settings.ES_HOST,
        'sleep': website.sleep_seconds,
        'expire_seconds': website.expire_seconds,
    }

    allow_domains = WebsiteAllowedDomain.objects.filter(website=website)
    task['allow_domains'] = [a.domain for a in allow_domains]

    start_urls = WebsiteUrlPattern.objects.filter(
        website=website, pattern_type=constant.URL_START)
    task['start_urls'] = [u.pattern for u in start_urls]

    walk_urls = WebsiteUrlPattern.objects.filter(
        website=website, pattern_type=constant.URL_WALK)
    task['walk_url_rules'] = [u.pattern for u in walk_urls]

    parse_urls = WebsiteUrlPattern.objects.filter(
        website=website, pattern_type=constant.URL_PARSE)
    task['parse_url_rules'] = [u.pattern for u in parse_urls]

    title_selector = WebsiteSelector.objects.get(
        website=website, key_name='title')
    task['title_selector'] = title_selector.xpath

    content_selector = WebsiteSelector.objects.get(
        website=website, key_name='body')
    task['content_selector'] = content_selector.xpath

    other_selectors = WebsiteSelector.objects.filter(
        website=website).exclude(
            key_name__in=['title', 'body'])
    task['custom_selectors'] = [
        {'field_name': s.key_name,
         'xpath': s.xpath}
        for s in other_selectors
    ]
    return task


def raw_es_query(index, query_body):
    es_host = settings.ES_HOST
    es = Elasticsearch(hosts=es_host)

    # query like raw_str
    if isinstance(query_body, str):
        res = es.search(
            index=index,
            doc_type='fulltext',
            body={
                'query': {
                    'multi_match': {
                        'query': query_body,
                        'fields': ['title', 'content']
                    }
                },
                'highlight': {
                    'fields': {
                        '*': {}
                    }
                }
            },
        )
    else:
        res = es.search(
            index=index,
            doc_type='fulltext',
            body={
                'query': {
                    'match': query_body
                },
                'highlight': {
                    'fields': {
                        '*': {}
                    }
                }
            },
        )
    return res


def es_query(data):
    query_data = data['query']
    ipp = data.get('ipp', 15)
    page = data.get('page', 1)
    index = data.get('index')

    res = raw_es_query(index, query_data)

    total = res['hits']['total']
    hits_data = []

    for hit in res['hits']['hits']:
        data = {
            'score': hit['_score'],
            'data': hit['highlight']
        }
        for field in ('url', 'title'):
            if field not in data['data']:
                data['data'][field] = hit['_source'][field]
        hits_data.append(data)

    str_pos = ipp * (page - 1)
    end_pos = ipp * page
    hits_data = hits_data[str_pos:end_pos]

    return {
        'page': page,
        'ipp': ipp,
        'total': total,
        'hits': hits_data
    }
