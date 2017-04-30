import json

from so import cache_keys
from so.cache import redis_cache
from so.models import Website, SpiderTask
from so.constant import constant


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
    spider_task.logs += '\n'.join(log_data)
    spider_task.save()


def run_task(task):
    website_id = task['website_id']
    spider_task = SpiderTask.objects.create(website_id=website_id,)
    task['task_id'] = spider_task.pk
    task_data = json.dumps(task)
    task_queue_key = cache_keys.key_of_task_queue()
    redis_cache.rpush(task_queue_key, task_data)
