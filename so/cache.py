from django_redis import get_redis_connection

redis_cache = get_redis_connection('default')
