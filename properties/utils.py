from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

def get_all_properties():
    """Existing utility to get/set properties cache."""
    queryset = cache.get('all_properties')
    if queryset is None:
        queryset = Property.objects.all()
        cache.set('all_properties', queryset, 3600)
    return queryset

def get_redis_cache_metrics():
    """
    Connects to Redis, retrieves performance metrics, 
    calculates the hit ratio, and logs the results.
    """
    # 1. Connect to Redis via django_redis
    con = get_redis_connection("default")
    
    # 2. Get info stats from Redis
    info = con.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    
    # 3. Calculate hit ratio
    total_requests = hits + misses
    hit_ratio = 0
    if total_requests > 0:
        hit_ratio = hits / total_requests

    # 4. Prepare metrics dictionary
    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': round(hit_ratio, 2),
        'total_requests': total_requests,
        'used_memory_human': info.get('used_memory_human', 'N/A')
    }

    # 5. Log metrics
    print(f"--- Redis Metrics ---")
    print(f"Hits: {hits} | Misses: {misses} | Ratio: {hit_ratio:.2f}")
    
    return metrics