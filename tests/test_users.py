
import pytest
from app import schemas
from .database import client, session
from jose import jwt
from app.config import settings

@pytest.fixture
def test_user(client):
    user_data = {'email':'helloworld12345@gmail.com',
                  'password':'helloworld1234'
                }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
    


def test_root(client):
    res = client.get('/')
    print(res.json().get('messeage'))
    assert res.json().get('messeage') == 'welcome to my api'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
        "/users/", json = {'email' : 'helloworld12345@gmail.com', 'password':'helloworld1234'}
    )
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == 'helloworld12345@gmail.com'
    assert res.status_code == 201

def test_login_user(test_user,client):
    res = client.post(
            "/login", data = {'username' : test_user['email'], 'password': test_user['password']}
        )
    login_res = schemas.Token(**res.json())
    #new_user = schemas.UserOut(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms = [settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



@pytest.mark.parametrize('email, password, status_code', [

    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    ('none', 'password123', 403),
    ('sanjeev@hotmail.com', 'none', 403)





])


def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        '/login', data ={ 'username': email, 'password': password}
    )

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'invalid credentials'


