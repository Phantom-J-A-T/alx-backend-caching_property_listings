from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieves all properties from Redis cache if available, 
    otherwise fetches from the database and caches the result for 1 hour.
    """
    # 1. Check Redis for 'all_properties'
    queryset = cache.get('all_properties')

    # 2. If not found, fetch from DB
    if queryset is None:
        queryset = Property.objects.all()
        
        # 3. Store the queryset in Redis for 3600 seconds (1 hour)
        cache.set('all_properties', queryset, 3600)
        print("Fetched from Database and cached.") # Optional: for debugging
    else:
        print("Fetched from Cache.") # Optional: for debugging

    return queryset