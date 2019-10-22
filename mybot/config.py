from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import pre


BOT_FATHER_TOKEN = '975397909:AAGPouov9vlfARRjsth_jPXT0j2rusHyCHM'
COINMARKETCAP_TOKEN = '58bb02ef-beb4-4da8-bdc7-2fc1b5ddf1a5'


class BUTTON:
    BTC = 'Курс BTC'
    ETH = 'Курс ETH'
    WALLET = 'Кошелек'
    HELP = 'Помощь'


class MESSAGE:
    START = emojize(f'Привет! Воспользуйтесь навигацией, '
                    'чтобы получить больше информации! :wink:')
    HELP = message_text = pre(emojize(
        '''Возможности бота:
- Показать курс криптовалюты :dollar:
- Отобразить баланс кошелька на основе id пользователя
- При написании любого сообщения, оно будет отправлено вам в ответ :speaker:'''
    ))
    SORRY = emojize(
        'Извините, произошла ошибка, попробуйте еще раз через некоторое '
        'время :worried:'
    )


class URL:

    class COINMARKETCAP:
        NAME = 'coinmarketcap'
        API = 'https://pro-api.coinmarketcap.com/v1'

    class DJANGOSERVER:
        NAME = 'djangoserver'


class CURRENCY:
    BTC = 'BTC'
    ETH = 'ETH'
    USD = 'USD'
    USDT = 'USDT'
