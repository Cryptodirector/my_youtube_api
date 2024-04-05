import os

import jwt

from fastapi import APIRouter, status

from app.users.service import UserService
from app.users.schemas import UserSchemas
from fastapi import Response, Request
from app.users.exceptions import Unauthorized

router = APIRouter(prefix='/api', tags=['Пользователь'])

SECRET_KEY = os.getenv('SECRET_KEY')
ALGO = os.getenv('ALGO')


@router.post('/registration')
async def registration_user(user: UserSchemas):
    await UserService.save_user(user=user.name, password=user.password)
    return {'detail': 'Вы успешно зарегистрировались!'}


@router.post('/login')
async def login_user(user: UserSchemas, response: Response):
    user_in = await UserService.login(
        user=user.name,
        password=user.password,
        response=response
    )
    if user_in:
        return {
            'status': 'success',
            'detail': 'Вы успешно авторизированы!',
            'status_code': status.HTTP_200_OK
        }

    elif user_in is None:
        raise Unauthorized


@router.patch('/users/update')
async def update_user(user: str, request: Request):
    cookie = request.cookies
    if cookie:
        return await UserService.update(user=user)

    else:
        raise Unauthorized


@router.post('/logout')
async def logout_user(response: Response):
    if response.delete_cookie(key='access_token_cookie'):
        return {
            'status': 'success',
            'detail': 'Вы вышли с аккаунта!',
            'status_code': status.HTTP_200_OK
        }


@router.get('/users/me')
async def read_current_user(
        request: Request
):
    if not request.cookies:
        raise Unauthorized

    else:
        for cookie in request.cookies.values():
            jwt_decode = jwt.decode(cookie, SECRET_KEY, algorithms=[ALGO])
            return {
                'status': 'success',
                'username': jwt_decode['subject']['username'],

                }
