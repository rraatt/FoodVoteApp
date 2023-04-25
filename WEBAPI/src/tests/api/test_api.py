import jwt
import pytest
from django.conf import settings
from django.contrib.auth.models import User

HEADERS = {
    'Accept': 'application/json; version=1.1'
}


@pytest.mark.django_db
def test_register_user(client):
    payload = {
        'username': 'tester',
        'password': 'Testpass69@',
        'email': 'abc@abc.com',
        'first_name': 'testname',
        'second_name': 'testsecondname'
    }

    response = client.post('/api/register/', data=payload, headers=HEADERS)

    assert 'access' in response.data
    assert 'refresh' in response.data

    # decode and verify access token
    access_token = response.data['access']
    try:
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        pytest.fail("Access token has expired")
    except jwt.InvalidTokenError:
        pytest.fail("Access token is invalid")

    # check that the user id in the token matches the registered user id
    assert decoded_token['user_id'] == User.objects.get(username='tester').id


@pytest.mark.django_db
def test_auth(user, client):
    response = client.post('/api/token/', data={'username': 'testuser',
                                                'password': 'password'}, headers=HEADERS)

    assert 'access' in response.data
    assert 'refresh' in response.data

    # decode and verify access token
    access_token = response.data['access']
    try:
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        pytest.fail("Access token has expired")
    except jwt.InvalidTokenError:
        pytest.fail("Access token is invalid")

    # check that the user id in the token matches the registered user id
    assert decoded_token['user_id'] == User.objects.get(username='testuser').id


@pytest.mark.django_db
def test_restaurant_create(client, admin_user):
    client.force_authenticate(user=admin_user)

    data = {'username': 'tester',
            'password': 'Testpass69@',
            'email': 'abc@abc.com',
            'first_name': 'testname',
            'second_name': 'testsecondname',
            'restaurant_name': 'test_restaurant',
            'restaurant_description': 'test_desc'}

    # Make a request to an endpoint that requires admin rights
    response = client.post('/api/newrestaurant/', data=data, headers=HEADERS)
    assert response.status_code == 200
    assert response.data['message'] == 'User account and restaurant entry created successfully'


@pytest.mark.django_db
def test_restaurant_create_fail(client, user):
    client.force_authenticate(user=user)

    data = {'username': 'tester',
            'password': 'Testpass69@',
            'email': 'abc@abc.com',
            'first_name': 'testname',
            'second_name': 'testsecondname',
            'restaurant_name': 'test_restaurant',
            'restaurant_description': 'test_desc'}
    response = client.post('/api/newrestaurant/', data=data, headers=HEADERS)
    assert response.status_code == 403


@pytest.mark.django_db
def test_creating_menu(client, restaurant_user):
    client.force_authenticate(user=restaurant_user)
    data = {
        'day': '2023-04-05',
        'content': 'food'
    }
    response = client.post('/api/menu/create/', data=data, headers=HEADERS)
    assert response.status_code == 201


@pytest.mark.django_db
def test_creating_menu(client, user):
    client.force_authenticate(user=user)
    data = {
        'day': '2023-04-05',
        'content': 'food'
    }
    response = client.post('/api/menu/create/', data=data, headers=HEADERS)
    assert response.status_code == 403


@pytest.mark.django_db
def test_voting(client, user, create_menus):
    client.force_authenticate(user=user)
    response = client.post('/api/vote/1/', headers=HEADERS)
    assert response.status_code == 200
    response = client.post('/api/vote/2/', headers=HEADERS)
    assert response.status_code == 403
