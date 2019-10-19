from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from .models import Account

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_result(data):
    if data:
        results = [user.to_json() for user in data]
    else:
        results = [{}]

    return results


@api_view(['POST'])
def get_users(request):
    id_ = request.POST['id']
    user = Account.objects.filter(user_id=id_)
    res = get_result(user)[0]
    return Response(res, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_users(request):
    id_ = request.POST['id']
    user_name = request.POST['user_name']
    balance = request.POST['balance']
    Account.objects.create(user_id=id_, user_name=user_name,
                           btc_balance=balance, eth_balance=balance)

    return Response([{}], status=status.HTTP_200_OK)


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
