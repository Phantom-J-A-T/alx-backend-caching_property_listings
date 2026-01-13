from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)  # Cache the result for 15 minutes
def property_list(request):
    """
    Fetches all properties and returns them as a JSON response.
    Subsequent requests within 15 mins will be served from Redis.
    """
    properties = Property.objects.all().values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    data = list(properties)
    return JsonResponse(data, safe=False)