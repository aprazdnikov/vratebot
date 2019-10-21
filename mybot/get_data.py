import time

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from accounts.models import Account

from mybot.requests_data import RequestData
from mybot.config import URL, COINMARKETCAP_TOKEN


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def users_start(user):
    if not get_users(user.id):
        create_users(user)


def users_wallet(user):
    return get_users(user.id)


def get_users(user_id):
    user = Account.objects.filter(user_id=user_id)
    return get_result(user)[0]


def create_users(user):
    balance = user.id
    Account.objects.create(
        user_id=user.id, user_name=user.full_name,
        btc_balance=balance, eth_balance=balance
    )


def get_result(data):
    if data:
        results = [user.to_json() for user in data]
    else:
        results = [{}]

    return results


def get_usdt():
    while True:
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKETCAP_TOKEN,
        }

        btc = URL.COINMARKETCAP.CURRENCY.BTC
        eth = URL.COINMARKETCAP.CURRENCY.ETH
        usdt = URL.COINMARKETCAP.CURRENCY.USDT

        r = RequestData(headers)
        currency = f"{btc},{eth}"
        results = r.get_data(
            service=URL.COINMARKETCAP.NAME,
            url=URL.COINMARKETCAP.API,
            param={'symbol': currency},
            currency=URL.COINMARKETCAP.CURRENCY.USDT
        )
        print(results)
        if results:
            for _ in results:
                data = _.get('data')
                if data.get('symbol') == btc:
                    cache.set(btc,
                              data.get('quote').get(usdt).get('price'),
                              timeout=CACHE_TTL)
                elif data.get('symbol') == eth:
                    cache.set(eth,
                              data.get('quote').get(usdt).get('price'),
                              timeout=CACHE_TTL)

        time.sleep(30)
