from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_start(count: int) -> InlineKeyboardMarkup:
    """
    Стартовая клавиатура для каждой роли
    :return:
    """
    logging.info('keyboard_start')
    button_1 = InlineKeyboardButton(text=f'Участвовать {count}', callback_data='participate')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboard_start_admin() -> ReplyKeyboardMarkup:
    """
    Стартовая клавиатура для каждой роли
    :return:
    """
    logging.info('keyboard_start_admin')
    button_1 = KeyboardButton(text='Провести розыгрыш')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                   resize_keyboard=True)
    return keyboard
