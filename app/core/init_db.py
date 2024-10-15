from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.database import Base
from app.models.notes import *

engine = create_async_engine(settings.DATABASE_URL) #движок для работы с БД

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# сессия для работы с БД


async def init_db(): #создание всех таблиц, если ее нет
    async with engine.begin() as connection: #открываем соединение с БД
        await connection.run_sync(Base.metadata.create_all)
        #при вызове init_db будем заупскать асинхронно функцию create_all, которая нам создаст все таблицы.

async def get_db():
    async with async_session.begin() as session:
        yield session
        #вернет результат, но работу не завершит, пока мы не завершим соедениение к БД
