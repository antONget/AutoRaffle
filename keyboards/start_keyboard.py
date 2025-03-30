from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging


def keyboard_start() -> ReplyKeyboardMarkup:
    """
    Стартовая клавиатура для каждой роли
    :return:
    """
    logging.info('keyboard_start')
    button_1 = KeyboardButton(text='🎁 Участвовать 🎁')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                   resize_keyboard=True)
    return keyboard


def keyboard_start_admin() -> ReplyKeyboardMarkup:
    """
    Стартовая клавиатура для каждой роли
    :return:
    """
    logging.info('keyboard_start_admin')
    button_1 = KeyboardButton(text='🎁 Участвовать 🎁')
    button_2 = KeyboardButton(text='🎉🏆 Провести розыгрыш 🚗✨')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1],
                                             [button_2]],
                                   resize_keyboard=True)
    return keyboard
