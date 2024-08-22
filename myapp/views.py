from django.shortcuts import render
# myapp/views.py
from myapp.models import Product

from django.core.cache import cache
from django.core.cache import caches
from django.http import HttpResponse
from django.shortcuts import render
import time

def expensive_computation():
    # Simulate a long computation
    time.sleep(5)
    return 'Computation Result'

def cached_view(request):
    # Try to get the result from the cache
    result = cache.get('expensive_result')

    if not result:
        # If not in cache, perform the computation
        result = expensive_computation()
        # Store the result in the cache for 10 minutes
        cache.set('expensive_result', result, timeout=600)

    return HttpResponse(f'The result is: {result}')

def product_list_view(request):
    # Try to get the product list from the cache
    product_list = cache.get('product_list')

    if not product_list:
        # If not in cache, query the database
        products = Product.objects.all()
        # Format the product list as a string
        product_list = ', '.join([f'{p.name} (${p.price})' for p in products])
        # Cache the result for 5 minutes
        cache.set('product_list', product_list, timeout=300)

    return HttpResponse(f'Products: {product_list}')






def my_view(request):
    # Accessing File-Based Cache (default)
    default_cache = caches['default']
    product_list = default_cache.get('product_list')
    if not product_list:
        # Fetch or generate product list
        product_list = ['Product 1', 'Product 2', 'Product 3']
        default_cache.set('product_list', product_list, timeout=3600)  # Cache in file for 1 hour
    
    # Accessing Database Cache (db_cache)
    db_cache = caches['db_cache']
    user_data = db_cache.get('user_data')
    if not user_data:
        # Fetch or generate user data
        user_data = {'name': 'John Doe', 'age': 30}
        db_cache.set('user_data', user_data, timeout=86400)  # Cache in database for 1 day
    
    return render(request, 'my_template.html', {'product_list': product_list,'user_data': user_data})


def cached_view(request):
    # Try to retrieve data from the cache
    data = cache.get('cached_data')
    
    if not data:
        # If data is not in the cache, generate or fetch it
        data = 'Some expensive data'  # Replace this with actual data fetching/generation logic
        
        # Store data in the cache for 1 hour (3600 seconds)
        cache.set('cached_data', data, timeout=3600)
    
    # Render a template and pass the cached data to it
    return render(request, 'cached_template.html', {'data': data})


# views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from .models import Article
from .serializers import ArticleSerializer

@api_view(['GET'])
def article_list_view(request):
    cache_key = 'article_list'
    cached_articles = cache.get(cache_key)
    
    if cached_articles is None:
        # Retrieve articles from the database
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        cached_articles = serializer.data
        # Cache the result with a timeout of 300 seconds (5 minutes)
        cache.set(cache_key, cached_articles, timeout=300)
    
    return Response(cached_articles)
