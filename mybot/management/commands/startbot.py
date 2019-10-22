import logging

from django.core.management.base import BaseCommand
from django.core.cache import cache

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

from mybot.config import BOT_FATHER_TOKEN, BUTTON, MESSAGE, CURRENCY

from mybot.keyboards import KeyboardsBot
from mybot.get_data import users_start, users_wallet, rate_currency


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
        price = rate_currency(msg.text.split(' ')[1])
        if price is not None:
            text_ = bold(f'{msg.text}: \n\n') + f"{price} USDT за единицу"
        else:
            text_ = MESSAGE.SORRY

    elif msg.text == BUTTON.WALLET:
        res = users_wallet(msg.from_user)
        if res:
            btc = res.get('btc')
            eth = res.get('eth')

            text_ = bold(
                f"{res.get('user_name')}\n\n") + \
                f"В вашем кошельке: \n" + \
                bold(CURRENCY.BTC) + f": {btc}\n" + \
                bold(CURRENCY.ETH) + f": {eth}"

            usdt = {
                CURRENCY.BTC: rate_currency(CURRENCY.BTC),
                CURRENCY.ETH: rate_currency(CURRENCY.ETH)
            }
            if (usdt.get(CURRENCY.BTC) is not None) and \
                    (usdt.get(CURRENCY.ETH) is not None):

                btc_to_usdt = float(btc) * float(usdt.get(CURRENCY.BTC))
                eth_to_usdt = float(eth) * float(usdt.get(CURRENCY.ETH))

                text_ += f"\n\n В валюте USDT:\n" \
                    f"{CURRENCY.BTC}: {str(btc_to_usdt)}\n" \
                    f"{CURRENCY.ETH}: {str(eth_to_usdt)}"

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
