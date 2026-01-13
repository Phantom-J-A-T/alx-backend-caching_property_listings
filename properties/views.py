from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    """
    View to return property listings using low-level cache utility.
    """
    # Use the utility function instead of direct DB query
    properties_qs = get_all_properties()
    
    # Convert queryset to list of dicts for JSON serialization
    data = list(properties_qs.values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    ))
    
    return JsonResponse({
        "status": "success",
        "data": data
    })