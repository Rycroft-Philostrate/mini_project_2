from unittest.mock import patch, Mock

import pytest

import project.tools.security
from project.exceptions import ItemNotFound
from project.models import User
from project.services import UserService


class TestUsersService:

    @pytest.fixture()
    @patch('project.dao.GenresDAO')
    def users_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = User(id=1, email="user@mail", password="Ll+ELt6teHvJetNJunNqeCXfrMFuy4axx++vThbl8V0=", name="user", surname="userss", favorite_genre=1)
        dao.get_by_email.return_value = User(id=2, email="user_2@mail", password="Ll+ELt6teHvJetNJunNqeCXfrMFuy4axx++vThbl8V0=", name="user_2", surname="userss_2", favorite_genre=1)
        dao.update_partial.return_value = User(id=2, email="user_2@mail", password="Ll+ELt6teHvJetNJunNqeCXfrMFuy4axx++vThbl8V0=", name="user_22", surname="userss_2", favorite_genre=1)
        dao.create.return_value = User(id=3, email="user_3@mail", password="Ll+ELt6teHvJetNJunNqeCXfrMFuy4axx++vThbl8V0=", name="user_3", surname="userss_3", favorite_genre=1)

        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UserService(dao=users_dao_mock)

    @pytest.fixture
    def user_1(self, db):
        obj = User(email="user_3@mail", password="Ll+ELt6HUYuBHUqeCXfrMFuy4axx++vThbl8V0=", name="user_3", surname="userss_3", favorite_genre=2)
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_user(self, users_service, user_1):
        assert users_service.get_item(1)

    def test_user_not_found(self, users_dao_mock, users_service):
        users_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            users_service.get_item(10)

    def test_get_user_by_email(self, users_service):
        assert users_service.get_by_email("user_2@mail").name == "user_2"

    def test_user_by_email_not_found(self, users_dao_mock, users_service):
        users_dao_mock.get_by_email.return_value = None

        with pytest.raises(ItemNotFound):
            users_service.get_by_email("user_2@mail")

    def test_user_update_partial(self, users_service):
        users_service.update_partial({"name": "user_22"}, "user_2@mail")

    def test_user_create(self, users_service, user_1):
        data = {"email": "name", "password": "password"}
        assert users_service.create(data).name == "user_3"

    def test_user_update_password(self, users_service, user_1):
        data = {"password_1": "name", "password_2": "password"}
        assert users_service.update_password(data, "user_2@mail") == ('Bad Password', 401)


