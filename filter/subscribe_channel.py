from aiogram.filters import Filter
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner

from keyboards.start_keyboard import keyboard_start
from database.requests import get_list_users
from config_data.config import Config, load_config

config: Config = load_config()


class ChannelProtect(Filter):
    async def __call__(self, message: Message, bot: Bot):
        u_status_1 = await bot.get_chat_member(chat_id=-1002138809375, user_id=message.from_user.id)
        u_status_2 = await bot.get_chat_member(chat_id=-1002059878338, user_id=message.from_user.id)
        if isinstance(u_status_1, ChatMemberMember) or isinstance(u_status_1, ChatMemberAdministrator) \
                or isinstance(u_status_1, ChatMemberOwner):
            if isinstance(u_status_2, ChatMemberMember) or isinstance(u_status_2, ChatMemberAdministrator) \
                    or isinstance(u_status_2, ChatMemberOwner):
                return True
        list_users = await get_list_users()
        if isinstance(message, CallbackQuery):
            await message.answer('')
            await message.message.answer(
                text=f'Чтобы участвовать в розыгрыше, обязательное условие  подписка на каналы:\n\n'
                     f'<a href="https://t.me/+cL9DtBv-HcFmMGE6">➡️ ТАЧКИ С ЗАЗОРОМ</a>\n'
                     f'<a href="https://t.me/+6yGTwfUvRuA4YmZi">➡️ АВТОЗОР🏎️🚀🛩️</a>\n',
                reply_markup=keyboard_start(count=len(list_users)),
                parse_mode='html',
                disable_web_page_preview=True)
        else:
            await message.answer(text=f'Чтобы участвовать в розыгрыше, обязательное условие  подписка на канал '
                                      f' вакансию своей мечты подпишись на канал '
                                      f'<a href="{config.tg_bot.channel_name}">{config.tg_bot.channel_name}</a>',
                                 reply_markup=keyboard_start(count=len(list_users)),
                                 parse_mode='html',
                                 disable_web_page_preview=True)
        return False
