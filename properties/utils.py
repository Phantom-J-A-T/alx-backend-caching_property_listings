import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

# Set up a logger for the properties app
logger = logging.getLogger(__name__)

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
    calculates hit ratio, and logs results formally.
    """
    try:
        # 1. Connect to Redis via django_redis
        con = get_redis_connection("default")
        
        # 2. Get info stats from Redis
        info = con.info()
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        # 3. Calculate hit ratio using ternary operator for safety
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        # 4. Prepare metrics dictionary
        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'hit_ratio': round(hit_ratio, 2),
            'total_requests': total_requests,
        }

        # 5. Formal logging
        logger.info(f"Redis Metrics - Hits: {hits}, Misses: {misses}, Ratio: {hit_ratio:.2f}")
        
        return metrics

    except Exception as e:
        # 6. Error logging as requested
        logger.error(f"Failed to retrieve Redis metrics: {str(e)}")
        return {}