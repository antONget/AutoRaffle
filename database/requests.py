from database.models import async_session
from database.models import User, Prize
from sqlalchemy import select

import logging


"""USER"""


async def add_user(data: dict) -> None:
    """
    Добавление пользователя
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == data['tg_id']))
        if not user:
            session.add(User(**data))
            await session.commit()
        else:
            user.username = data['username']
            await session.commit()


async def get_user_by_id(tg_id: int) -> User:
    """
    Получение информации о пользователе по tg_id
    :param tg_id:
    :return:
    """
    logging.info('set_user_role')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_list_users() -> list[User]:
    """
    Получение информации о пользователях
    :return:
    """
    logging.info('get_list_users')
    async with async_session() as session:
        users = await session.scalars(select(User))
        return [user for user in users]


"""PRIZE"""


async def add_prize(count_prize: int, prize: str) -> None:
    """
    Добавление победителя
    :param count_prize:
    :param prize:
    :return:
    """
    logging.info(f'add_prize')
    async with async_session() as session:
        prize = await session.scalar(select(Prize).where(Prize.id == count_prize))
        if not prize:
            session.add(Prize(**{"name_prize": prize}))
            await session.commit()
        else:
            prize.name_prize = prize
            await session.commit()


async def get_list_prize() -> list[Prize]:
    """
    Получение информации о победителях
    :return:
    """
    logging.info('get_list_users')
    async with async_session() as session:
        prizes = await session.scalars(select(Prize))
        return [prize for prize in prizes]


async def get_prize(id_prize: int) -> Prize:
    """
    Добавление победителя
    :param id_prize:
    :return:
    """
    logging.info(f'get_prize')
    async with async_session() as session:
        return await session.scalar(select(Prize).where(Prize.id == id_prize))
