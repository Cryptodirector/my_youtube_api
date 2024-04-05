from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('name,password,status_code', [
    ('4iter', 'lamba', 200),
    ('Lam', '12234', 422),
    ('Lama4dfdas3fdssaq', '12234', 422),
    ('Lama4', '12', 422),
    ('Lama4df', '12234323213dsfsdfdsfsd', 422)
])
async def test_registration_user(name, password, status_code, ac: AsyncClient):
    response = await ac.post('api/registration', json={
        'name': name,
        'password': password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('name, password, status_code', [
    ('4iter', 'lamba', 200),
    ('string', 'string', 401),

])
async def test_login_user(name, password, status_code, ac: AsyncClient):
    response = await ac.post('api/login', json={
        'name': name,
        'password': password
    })

    assert response.status_code == status_code
