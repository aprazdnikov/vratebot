from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import collections


class RequestData(object):

    def __init__(self, token):
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': token,
        }
        self.session = Session()
        self.session.headers.update(self.headers)

    def get_data(self, url: str, parameters: dict):
        return self.__request(url, parameters)

    def __request(self, url, parameters):
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

        return None

    def __get_data_crypto(self, url, params):
        try:
            response = self.session.get(url, params=params)
            return json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return str(e)
