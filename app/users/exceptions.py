from fastapi import HTTPException, status


class AllException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class UserAlreadyException(AllException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'


class InvalidUserInput(AllException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Неверный логин или пароль'


class Unauthorized(AllException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Вы не зарегистрированы'