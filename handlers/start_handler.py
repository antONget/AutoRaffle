import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config_data.config import Config, load_config
from database import requests as rq
from database.models import User, Prize
from utils.error_handling import error_handler
from keyboards.start_keyboard import keyboard_start, keyboard_start_admin
from filter.subscribe_channel import ChannelProtect
from filter.admin_filter import check_super_admin, IsSuperAdmin

import logging

router = Router()
config: Config = load_config()


class NumRaffle(StatesGroup):
    number = State()


@router.message(CommandStart())
@error_handler
async def process_start_command_user(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обработки запуска бота или ввода команды /start
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_start_command_user: {message.from_user.id}')
    await state.set_state(state=None)
    # добавление пользователя в БД если еще его там нет
    user: User = await rq.get_user_by_id(tg_id=message.from_user.id)
    if not user:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "user_name"
        data_user = {"tg_id": message.from_user.id,
                     "username": username,
                     "role": "role"}
        await rq.add_user(data=data_user)
    else:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "user_name"
        data_user = {"tg_id": message.from_user.id,
                     "username": username}
        await rq.add_user(data=data_user)
    list_users: list[User] = await rq.get_list_users()
    if await check_super_admin(telegram_id=message.from_user.id):
        await message.answer(text=f'Для участия в розыгрыше зарегистрировалось {len(list_users)} человек.\n '
                                  f'Для проведения розыгрыша нажмите кнопку "Провести розыгрыш"',
                             reply_markup=keyboard_start())
    else:
        await message.answer_photo(
            photo='AgACAgIAAxkBAAMgZ-lXo13TR8TNLSK_tC2t2yTYoLIAAqnsMRuYcFFL3zh9Nt2n88QBAAMCAAN4AAM2BA',
            caption=f'Здравствуйте! Мы рады видеть вас в нашем боте!\n'
                    f'Здесь у вас есть уникальная возможность выиграть шикарный автомобиль абсолютно бесплатно!\n\n'
                    f'Для участия:\n'
                    f'1. Подписаться на наши 2 канала:\n\n'
                    f'<a href="https://t.me/+cL9DtBv-HcFmMGE6">➡️ ТАЧКИ С ЗАЗОРОМ</a>\n\n'
                    f'<a href="https://t.me/+6yGTwfUvRuA4YmZi">➡️ АВТОЗОР🏎️🚀🛩️</a>\n\n'
                    f'2. Нажмите кнопку "Участвовать" ниже. 👇\n'
                    f'3. Следите за новостями и ждите розыгрыша! Он будет проводиться в прямом эфире.\n'
                    f'🔔 Не забудьте пригласить друзей!\n Пусть удача будет на вашей стороне!',
            reply_markup=keyboard_start(count=len(list_users)))


@router.callback_query(F.data == 'participate', ChannelProtect())
@error_handler
async def process_registaration(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Регистрация на розыгрыш
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_registaration: {message.from_user.id}')
    await message.answer(text="""📢 Дорогие участники!

Мы благодарим вас за участие в нашем конкурсе по розыгрышу автомобиля! 🚗 Вам присвоен индивидуальный номер.

Ваше стремление вдохновляют нас, и мы рады видеть такой широкий интерес к нашему мероприятию. 
Каждый из вас стал важной частью этого захватывающего события!

Следите за обновлениями, ведь совсем скоро мы объявим победителя! Удачи всем! 🍀""")


@router.message(F.text == '🎉🏆 Провести розыгрыш 🚗✨', IsSuperAdmin())
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
    await message.answer(text='Пришлите номер участника для объявления его победителем')
    await state.set_state(NumRaffle.number)


@router.message(StateFilter(NumRaffle.number), IsSuperAdmin())
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
    if message.text.isdigit():
        await state.set_state(state=None)
        data = await state.get_data()

        count = 1
        if data.get('count_raffle'):
            count = data['count_raffle'] + 1
            if count == 4:
                await state.clear()
                await message.answer(text='Все призы разыграны, поздравляю победителей!')
                return

        await state.update_data(count_raffle=count)
        # raffle_user = ['1 й победитель айфон-@Maksim_Ipatov',
        #                '2 й победитель жигули- @Oleg_Maksimovichh',
        #                '3 й победитель бмв- @VVK0404']
        prize: Prize = await rq.get_prize(id_prize=count)
        msg = await message.answer(text='Уже ищу в журнале зарегистрированных победителя...')
        msg_ = await message.answer_sticker(
            sticker='CAACAgQAAxkBAAMhZ-lX90pMKhrirF-HzdWwxki6OecAAkkDAALN9cAEs75ahlKdplY2BA')
        await asyncio.sleep(3)
        await msg.delete()
        await msg_.delete()
        await message.answer(text=f"""🎉🏆 Поздравляю победителя нашего розыгрыша! ✨
    
С радостью объявляю имя счастливчика:
    
    {count}-й победитель {prize.name_prize}
    
🥳 Спасибо всем участникам за участие! Не забудьте следить за нашими анонсами
    , ведь впереди еще много интересных розыгрышей и акций!
    
🎊 Поздравляем еще раз!""")
    else:
        await message.answer(text='Для объявления победителя мне нужно число')
