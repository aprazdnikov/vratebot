import logging

from django.core.management.base import BaseCommand
from django.core.cache import cache

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

from mybot.config import BOT_FATHER_TOKEN, COINMARKETCAP_TOKEN, \
    BUTTON, MESSAGE, URL

from mybot.keyboards import KeyboardsBot
from mybot.requests_data import RequestData
from mybot.get_data import users_start, users_wallet


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_FATHER_TOKEN)
dp = Dispatcher(bot)
kb = KeyboardsBot()


class Command(BaseCommand):
    help = 'Start my bot'

    def handle(self, *args, **options):
        if options['bot']:
            executor.start_polling(dp)

    def add_arguments(self, parser):
        parser.add_argument(
            '-b',
            '--bot',
            default=False,
            action='store_true',
            help='Запускает телеграм бота'
        )


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    users_start(message.from_user)
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
            service=URL.COINMARKETCAP.NAME,
            url=URL.COINMARKETCAP.API,
            param={'symbol': msg.text.split(' ')[1]},
            currency=URL.COINMARKETCAP.CURRENCY.USDT
        )
        if price is not None:
            text_ = bold(f'{msg.text}: \n\n') + f"{price} USDT за единицу"
        else:
            text_ = MESSAGE.SORRY

    elif msg.text == BUTTON.WALLET:
        res = users_wallet(msg.from_user)
        if res:
            text_ = bold(
                f"{res.get('user_name')}\n\n") + \
                f"В вашем кошельке: \n" + \
                bold(f"BTC:") + f" {res.get('btc')}\n" + \
                bold(f"ETH:") + f" {res.get('eth')}"
            if URL.COINMARKETCAP.CURRENCY.BTC in cache:
                text_ += f"\n\n В валюте USDT:\n" \
                    f"BTC: {cache.get(URL.COINMARKETCAP.CURRENCY.BTC)}"
            if URL.COINMARKETCAP.CURRENCY.ETH in cache:
                text_ += f"\nETH: {cache.get(URL.COINMARKETCAP.CURRENCY.BTC)}"

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
