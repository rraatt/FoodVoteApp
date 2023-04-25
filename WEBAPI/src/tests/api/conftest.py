import uuid

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from foodapp.models import Restaurant, Menu


@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password'
    )
    return user


@pytest.fixture
def create_menus():
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser12',
        email='testuser@example.com',
        password='password'
    )
    restaurant = Restaurant.objects.create(name='test', description='Lore ipsum', owner=user)
    restaurant.save()
    restaurant2 = Restaurant.objects.create(name='test2', description='Lore ipsum2', owner=user)
    restaurant2.save()
    menu1 = Menu.objects.create(day=timezone.now().date(), content='content1', owner=restaurant)
    menu1.save()
    menu1 = Menu.objects.create(day=timezone.now().date(), content='content2', owner=restaurant2)
    menu1.save()


@pytest.fixture
def restaurant_user():
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='password'
    )
    restaurant = Restaurant.objects.create(name='test', description='Lore ipsum', owner=user)
    restaurant.save()
    return user


@pytest.fixture
def admin_user():
    """Create and return an admin user"""
    user = User.objects.create_user('admin', password='adminpass')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def client():
    return APIClient()
