from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import BUTTON


class KeyboardsBot(object):

    def __init__(self):
        self.btn_btc = KeyboardButton(BUTTON.BTC)
        self.btn_eth = KeyboardButton(BUTTON.ETH)
        self.btn_help = KeyboardButton(BUTTON.HELP)
        self.btn = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).row(self.btn_btc, self.btn_eth).add(self.btn_help)
