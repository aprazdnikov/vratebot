import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

from mybot.config import BOT_FATHER_TOKEN, COINMARKETCAP_TOKEN, \
    BUTTON, MESSAGE, URL
from mybot.keyboards import KeyboardsBot
from mybot.requests_data import RequestData


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_FATHER_TOKEN)
dp = Dispatcher(bot)
kb = KeyboardsBot()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user = message.from_user
    r = RequestData()
    res = r.get_data(
        URL.DJANGOSERVER.NAME, URL.DJANGOSERVER.GET, {'id': user.id}
    )
    if not res:
        r.get_data(
            URL.DJANGOSERVER.NAME, URL.DJANGOSERVER.CREATE,
            {'id': user.id, 'user_name': user.full_name, 'balance': user.id}
        )

    await message.reply(MESSAGE.START, reply_markup=kb.btn)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGE.HELP, reply_markup=kb.btn)


@dp.message_handler()
async def echo_message(msg: types.Message):

    if (msg.text == BUTTON.BTC) or (msg.text == BUTTON.ETH):
        r = RequestData(
            header={'Accepts': 'application/json',
                    'X-CMC_PRO_API_KEY': COINMARKETCAP_TOKEN}
            )
        price = r.get_data(
            name_service=URL.COINMARKETCAP.NAME,
            url=URL.COINMARKETCAP.API,
            parameters={'symbol': msg.text.split(' ')[1]}
        )
        if price is not None:
            text_ = bold(f'{msg.text}: \n\n') + f"{price} USD за единицу"
        else:
            text_ = MESSAGE.SORRY

    elif msg.text == BUTTON.WALLET:
        r = RequestData()
        res = r.get_data(
            URL.DJANGOSERVER.NAME, URL.DJANGOSERVER.GET,
            {'id': msg.from_user.id}
        )
        if res:
            text_ = bold(
                f"{res.get('user_name')}\n\n") + \
                f"В вашем кошельке: \n" + \
                bold(f"BTC:") + f" {res.get('btc')}\n" + \
                bold(f"ETH:") + f" {res.get('eth')}"
        else:
            text_ = MESSAGE.SORRY

    elif msg.text == BUTTON.HELP:
        text_ = MESSAGE.HELP

    else:
        text_ = msg.text

    await bot.send_message(
        msg.from_user.id, text_,
        reply_markup=kb.btn, parse_mode=ParseMode.MARKDOWN
    )


if __name__ == '__main__':
    executor.start_polling(dp)
