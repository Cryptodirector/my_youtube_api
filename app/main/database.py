import os
from dotenv import load_dotenv, find_dotenv
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv(find_dotenv())

MODE = os.getenv('MODE')
TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_POSTGRES_USER = os.environ.get("TEST_DB_USER")
TEST_POSTGRES_PASSWORD = os.environ.get("TEST_DB_PASS")
TEST_POSTGRES_DB = os.environ.get("TEST_DB_NAME")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
POSTGRES_USER = os.environ.get("DB_USER")
POSTGRES_PASSWORD = os.environ.get("DB_PASS")
POSTGRES_DB = os.environ.get("DB_NAME")


if MODE == 'TEST':
    DATABASE_URL = (f'postgresql+asyncpg://{TEST_POSTGRES_USER}:{TEST_POSTGRES_PASSWORD}@{TEST_DB_HOST}:'
                    f'{TEST_DB_PORT}/{TEST_POSTGRES_DB}')
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}'
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
