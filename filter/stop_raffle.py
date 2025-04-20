from aiogram.filters import Filter
from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from config_data.config import Config, load_config
from datetime import datetime

config: Config = load_config()


class StopRaffel(Filter):
    async def __call__(self, message: Message, bot: Bot):
        current_time = datetime.now()
        check_time = datetime.strptime('20.04.2025 16:00', '%d.%m.%Y %H:%M')
        if current_time < check_time:
            return True
        if isinstance(message, CallbackQuery):
            await message.message.answer(
                text="""Розыгрыш проведен✅

Победители 🏆 :

@Nemo0o0o

@sonikkk228

@tetvont96""")
        else:
            await message.answer(text="""Розыгрыш проведен✅

Победители 🏆 :

@Nemo0o0o

@sonikkk228

@tetvont96""")
        return False
