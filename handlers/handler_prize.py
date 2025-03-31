import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config_data.config import Config, load_config
from database import requests as rq
from database.models import Prize
from utils.error_handling import error_handler

from filter.admin_filter import IsSuperAdmin

import logging

router = Router()
config: Config = load_config()


class PrizeState(StatesGroup):
    prize = State()


@router.message(F.text == '/add_raffle', IsSuperAdmin())
@error_handler
async def process_add_raffle(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Добавление победителей
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_add_raffle: {message.from_user.id}')
    await message.answer(text=f'Пришлите сведения для 1-го победителя,'
                              f' например: айфон-@Maksim_Ipatov')
    await state.set_state(PrizeState.prize)


@router.message(StateFilter(PrizeState.prize), IsSuperAdmin())
@error_handler
async def process_ruffle(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Проведение розыгрыша
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_ruffle: {message.from_user.id}')
    data = await state.get_data()
    count_prize = 2
    if data.get('count_prize'):
        count_prize = data['count_prize'] + 1
        if count_prize == 4:
            await rq.add_prize(count_prize=count_prize - 1, prize_str=message.text)
            await state.clear()
            await state.update_data(count_prize=count_prize)
            list_prizes: list[Prize] = await rq.get_list_prize()
            text = 'Победители успешно добавлены:\n\n'
            for i, prize in enumerate(list_prizes):
                text += f'{i+1}. {prize.name_prize}\n'
            await message.answer(text=text)
            return
    await rq.add_prize(count_prize=count_prize-1, prize_str=message.text)
    await state.update_data(count_prize=count_prize)
    await message.answer(text=f'Пришлите сведения для {count_prize}-го победителя,'
                              f' например: айфон-@Maksim_Ipatov')
