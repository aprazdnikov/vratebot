from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from .config import URL

import json
import collections


class RequestData(object):

    def __init__(self, header=None):
        self.session = Session()
        if header is not None:
            self.session.headers.update(header)

    def get_data(self, service: str, url: str, param: dict, currency=None):
        return self.__request(service, url, param, currency)

    def __request(self, name_service, url, parameters, currency):

        if name_service == URL.COINMARKETCAP.NAME:
            id_crypto = self.__get_data_crypto(
                f"{url}/cryptocurrency/map", parameters
            )

            if isinstance(id_crypto, collections.Mapping):
                price = []
                for _ in id_crypto.get('data'):
                    id_ = _.get('id')
                    price.append(self.__get_data_crypto(
                        f"{url}/tools/price-conversion",
                        {'id': id_, 'amount': '1', 'convert': currency}
                    ))

                if isinstance(price, collections.Mapping):
                    if len(price) > 1:
                        return price
                    else:
                        return str(round(price.get('data').get('quote')
                                         .get(currency).get('price'), 2))
        else:
            return None

    def __get_data_crypto(self, url, params):
        try:
            response = self.session.get(url, params=params)
            return json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return str(e)
