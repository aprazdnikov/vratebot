from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import pre


BOT_FATHER_TOKEN = '975397909:AAGPouov9vlfARRjsth_jPXT0j2rusHyCHM'
COINMARKETCAP_TOKEN = '58bb02ef-beb4-4da8-bdc7-2fc1b5ddf1a5'


class BUTTON:
    BTC = 'BTC'
    ETH = 'ETH'
    WALLET = 'Кошелек'
    HELP = 'Помощь'


class MESSAGE:
    START = emojize('Привет! Воспользуйтесь клавиатурой, '
                    'чтобы получить больше информации! :wink:')
    HELP = message_text = pre(emojize(
        '''Возможности бота:
- Показать курс криптовалюты :dollar:
- При написании любого сообщение, оно будет отправлено вам в ответ :speaker:'''
    ))
    SORRY = emojize(
        'Извините, произошла ошибка, попробуйте еще раз через некоторое '
        'время :worried:'
    )


class URL:
    class COINMARKETCAP:
        NAME = 'coinmarketcap'
        API = 'https://pro-api.coinmarketcap.com/v1'

    class DJANGO_SERVER:
        NAME = 'djangoserver'
        GET = 'http://127.0.0.1:8000/users/get'
        CREATE = 'http://127.0.0.1:8000/users/create'
