from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


# Создаем асинхронный движок
engine = create_async_engine("sqlite+aiosqlite:///database/db.sqlite3", echo=False)
# Настраиваем фабрику сессий
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default='user')


class Prize(Base):
    __tablename__ = 'prizes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_prize: Mapped[str] = mapped_column(String, nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
