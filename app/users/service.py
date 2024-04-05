from app.main.database import async_session_maker
from sqlalchemy import select, insert, update

from datetime import timedelta
from app.users.security import Hasher, access_security
from app.users.models import User
from fastapi import Response, status
from sqlalchemy.exc import IntegrityError
from app.users.exceptions import UserAlreadyException, InvalidUserInput, Unauthorized


class UserService:
    @staticmethod
    async def save_user(user, password):
        async with async_session_maker() as session:
            hash_password = Hasher.get_password_hash(password)

            try:
                query = insert(User).values(name=user, password=hash_password)
                await session.execute(query)
                await session.commit()

            except IntegrityError:
                return UserAlreadyException

    @staticmethod
    async def login(user, password, response: Response):
        async with async_session_maker() as session:
            stmt = select(User).where(User.name == user)
            result = await session.execute(stmt)
            for results in result.scalars():

                if user == results.name:
                    plain_pass = Hasher.verify_password(
                        plain_password=password,
                        hashed_password=results.password
                    )

                    if plain_pass is True:
                        subject = {"username": user}
                        access_token = access_security.create_access_token(subject=subject)
                        access_security.set_access_cookie(
                            response,
                            access_token,
                            expires_delta=timedelta(days=5)
                        )
                        return {'access_token': access_token}

                    else:
                        raise InvalidUserInput
                else:
                    raise InvalidUserInput

    @staticmethod
    async def update(user: str):
        async with async_session_maker() as session:
            query = update(User).values(name=user)
            await session.execute(query)
            await session.commit()
            return {
                'status': 'success',
                'detail': 'Ваше имя успешно обновленно!',
                'status_code': status.HTTP_200_OK
            }