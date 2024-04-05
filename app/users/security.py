import os

from fastapi_jwt import JwtAccessBearer
from passlib.context import CryptContext
from fastapi import Request
import jwt


SECRET_KEY = os.getenv('SECRET_KEY')
ALGO = os.getenv('ALGO')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_security = JwtAccessBearer(secret_key=SECRET_KEY, auto_error=True)


async def get_cookie(request: Request):
    for cookie in request.cookies.values():
        user = jwt.decode(cookie, SECRET_KEY, algorithms=[ALGO])
        return user['subject']['username']


class Hasher:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)