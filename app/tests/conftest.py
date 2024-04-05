import asyncio
import os

import pytest
from sqlalchemy import insert

from app.main.database import Base, async_session_maker, engine

from app.main.models import Comments, Video
from app.users.models import User

from httpx import AsyncClient, ASGITransport
from main import app as fastapi_app

MODE = os.getenv('MODE')


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # async with async_session_maker() as session:
    #     add_users = insert(User).values(name='slavik', password='34432423423')
    #     add_video = insert(Video).values(
    #         title='БАРАН',
    #         description='баран есть утенка',
    #         link='youtube.com',
    #         id_user=1
    #     )
    #     add_comment = insert(Comments).values(
    #         text='ГОВНЕО',
    #         id_user=1,
    #         id_video=1
    #     )
    #     await session.execute(add_users)
    #     await session.execute(add_video)
    #     await session.execute(add_comment)
    #     await session.commit()


@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session