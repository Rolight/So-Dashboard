import json

from so import cache_keys
from so.cache import redis_cache


def get_spiders():
    cluster_key = cache_keys.key_of_spider_cluster()
    all_spiders = [s.decode() for s in redis_cache.smembers(cluster_key)]
    spiders = {}
    for spider in all_spiders:
        spider_key = cache_keys.key_of_spider(spider)
        spider_data = redis_cache.get(spider_key)
        if spider_data is not None:
            spiders[spider] = json.loads(spider_data.decode())
    return {'all_spiders': all_spiders, 'spiders': spiders}
