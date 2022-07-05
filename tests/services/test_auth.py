from unittest.mock import patch

import pytest

from jwt.exceptions import DecodeError
from project.models import User
from project.services import AuthService


class TestAuthService:

    @pytest.fixture()
    @patch('project.services.UserService')
    def users_service_mock(self, service_mock):
        service = service_mock()
        service.get_by_email.return_value = User(id=1, email="user@mail", password="UXl4fhdsolojOWwGWqg7tzzg1bQASYjQ2HrAVEqLwzI=", name="user", surname="userss", favorite_genre=1)
        return service

    @pytest.fixture()
    def auth_service(self, users_service_mock):
        return AuthService(user_service=users_service_mock)

    @pytest.fixture
    def user_1(self, db):
        obj = User(email="user_3@mail", password="Ll+ELt6HUYuBHUqeCXfrMFuy4axx++vThbl8V0=", name="user_3",
                   surname="userss_3", favorite_genre=2)
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_create_token(self, auth_service, user_1):
        assert 'access_token' in auth_service.create_token("user@mail", "user")

    def test_create_token_bad_email(self, auth_service, users_service_mock):
        users_service_mock.get_by_email.return_value = None
        assert auth_service.create_token("user55@mail", "user") == ('Bad Email', 401)

    def test_check_refresh_token(self, auth_service, user_1):
        with pytest.raises(DecodeError):
            auth_service.check_refresh_token('eyJ0eXAiiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InVzZXJAbWFpbCIsImV4cCI6MTY1OTYwMTc4Mn0.Zp-FvG0uGsTxYV5')
