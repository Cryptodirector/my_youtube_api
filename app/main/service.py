import os

from sqlalchemy import select, insert, delete, and_, update
from app.main.database import async_session_maker
from app.main.models import Comments
from fastapi import Request

from app.main.schemas import AddVideoSchemas, UpdateVideoSchemas, AddCommentSchemas
from app.users.models import User
from app.main.models import Video

from app.users.security import get_cookie


SECRET_KEY = os.getenv('SECRET_KEY')
ALGO = os.getenv('ALGO')


class MainService:

    @staticmethod
    async def get_all_video():
        async with async_session_maker() as session:
            query = select(Video.title, Video.link, User.name).join(
                User,
                User.id == Video.id_user
            )
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def add_video(video: AddVideoSchemas, request: Request):
        user = await get_cookie(request)
        async with async_session_maker() as session:
            query = select(User.id).where(User.name == user)
            result = await session.execute(query)
            stmt = insert(Video).values(
                title=video.title,
                description=video.descriptions,
                link=video.link,
                id_user=result.scalar()
            )
            await session.execute(stmt)
            await session.commit()
            return {'detail': 'Видео успешно добавлено!'}

    @staticmethod
    async def look_my_video(request: Request):
        user = await get_cookie(request)
        async with async_session_maker() as session:
            subq = select(User.id).where(User.name == user)
            id_user = await session.execute(subq)
            query = select(
                Video.title,
                Video.description,
                Video.link,
                Video.id,
                User.name
            ).join(User).where(Video.id_user == id_user.scalar())
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def delete_my_video(id: int):

        async with async_session_maker() as session:
            video = delete(Video).where(Video.id == id)
            await session.execute(video)
            await session.commit()
            return {'detail': 'Видео удалено!'}

    @staticmethod
    async def search_video(title: str):
        async with async_session_maker() as session:
            video = select(
                Video.title,
                Video.link,
                User.name
            ).join(User).filter(Video.title.like(f'%{title}%'))
            result = await session.execute(video)
            return result.mappings().all()

    @staticmethod
    async def change_video(video: UpdateVideoSchemas):
        async with async_session_maker() as session:
            stmt = update(Video).where(Video.id == video.id).values(
                title=video.title,
                description=video.description
            )
            await session.execute(stmt)
            await session.commit()
            return {'detail': 'Ваше видео обновлено!'}

    @staticmethod
    async def add_comment(
            request: Request,
            comment: AddCommentSchemas,
            id_video: int
    ):
        user = await get_cookie(request)
        async with async_session_maker() as session:
            query = select(User.id).where(User.name == user)
            id = await session.execute(query)

            stmt = insert(Comments).values(
                text=comment.text,
                id_video=id_video,
                id_user=id.scalar()
            )
            await session.execute(stmt)
            await session.commit()
            return {'detail': 'Комментарий создан!'}

    @staticmethod
    async def change_comment(
            request: Request,
            id: int,
            comments: AddCommentSchemas
    ):
        user = await get_cookie(request)
        async with async_session_maker() as session:
            subq = select(User.id).where(User.name == user)
            id_user = await session.execute(subq)
            stmt = update(Comments).where(
                and_(
                    Comments.id_user == id_user.scalar(),
                    Comments.id == id
                )
            ).values(text=comments.text)
            await session.execute(stmt)
            await session.commit()
            return {'detail': 'Комментарий изменен!'}

    @staticmethod
    async def delete_comment(
            request: Request,
            id: int,
    ):
        user = await get_cookie(request)
        async with async_session_maker() as session:
            subq = select(User.id).where(User.name == user)
            id_user = await session.execute(subq)
            stmt = delete(Comments).where(
                and_(
                    Comments.id_user == id_user.scalar(),
                    Comments.id == id
                )
            )
            await session.execute(stmt)
            await session.commit()
            return {'detail': 'Комментарий удален!'}