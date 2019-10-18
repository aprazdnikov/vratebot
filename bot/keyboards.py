from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from .config import BUTTON


class KeyboardsBot(object):

    def __init__(self):
        self.btn_btc = KeyboardButton(BUTTON.BTC)
        self.btn_eth = KeyboardButton(BUTTON.ETH)
        self.btn_wallet = KeyboardButton(BUTTON.WALLET)
        self.btn_help = KeyboardButton(BUTTON.HELP)
        self.btn = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).row(self.btn_btc, self.btn_eth)\
            .row(self.btn_help, self.btn_wallet)
