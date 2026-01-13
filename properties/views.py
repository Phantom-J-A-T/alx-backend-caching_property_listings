from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property


@cache_page(60 * 15)
def property_list(request):
    """
    Returns all properties wrapped in a JSON object.
    """
    properties = Property.objects.all().values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    
    # Wrapping the list in a dictionary for a cleaner API response
    return JsonResponse({
        "status": "success",
        "data": list(properties)
    })