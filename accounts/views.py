from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import Account

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
@api_view(['GET'])
def view_cached_users(request):
    if 'account' in cache:
        users = cache.get('account')
        return Response(users, status=status.HTTP_201_CREATED)
    else:
        users = Account.objects.all()
        results = [user.to_json() for user in users]
        cache.set('account', results, timeout=CACHE_TTL)
        return Response(results, status=status.HTTP_201_CREATED)
