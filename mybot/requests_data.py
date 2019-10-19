from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from .config import URL

import json
import collections


class RequestData(object):

    def __init__(self, header=None):
        self.session = Session()
        if header is not None:
            self.session.headers.update(header)

    def get_data(self, name_service: str, url: str, parameters: dict):
        return self.__request(name_service, url, parameters)

    def __request(self, name_service, url, parameters):
        if name_service == URL.COINMARKETCAP.NAME:
            id_crypto = self.__get_data_crypto(
                f"{url}/cryptocurrency/map", parameters
            )
            if isinstance(id_crypto, collections.Mapping):
                _ = id_crypto.get('data')[0].get('id')
                price = self.__get_data_crypto(
                    f"{url}/tools/price-conversion",
                    {'id': _, 'amount': '1', 'convert': 'USD'}
                )
                if isinstance(price, collections.Mapping):
                    _ = price.get('data').get('quote').get('USD').get('price')
                    return str(round(_, 2))
        elif name_service == URL.DJANGOSERVER.NAME:
            return self.__data_in_base(url, parameters)

        else:
            return None

    def __get_data_crypto(self, url, params):
        try:
            response = self.session.get(url, params=params)
            return json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return str(e)

    def __data_in_base(self, url, params):
        try:
            response = self.session.post(url, data=params)
            return json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return str(e)