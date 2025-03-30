from aiogram.filters import Filter
from aiogram.types import Message
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner

from config_data.config import Config, load_config

config: Config = load_config()


class ChannelProtect(Filter):
    async def __call__(self, message: Message, bot: Bot):
        u_status = await bot.get_chat_member(chat_id=config.tg_bot.channel_name, user_id=message.from_user.id)
        if isinstance(u_status, ChatMemberMember) or isinstance(u_status, ChatMemberAdministrator) \
                or isinstance(u_status, ChatMemberOwner):
            return True
        if isinstance(message, CallbackQuery):
            await message.answer('')
            await message.message.answer(text=f'Чтобы участвовать в розыгрыше, обязательное условие  подписка на канал '
                                              f'<a href="{config.tg_bot.channel_name}">'
                                              f'{config.tg_bot.channel_name}</a>',
                                         parse_mode='html')
        else:
            await message.answer(text=f'Чтобы участвовать в розыгрыше, обязательное условие  подписка на канал '
                                      f' вакансию своей мечты подпишись на канал '
                                      f'<a href="{config.tg_bot.channel_name}">{config.tg_bot.channel_name}</a>',
                                 parse_mode='html')
        return False
