import pytest

from project.dao import UsersDAO
from project.models import User


class TestUserDAO:
    @pytest.fixture
    def users_dao(self, db):
        return UsersDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        g = User(email="user@mail", password="Ll+ELt6teHvJetNJunNqeCXfrMFuy4axx++vThbl8V0=", name="user", surname="userss", favorite_genre=1)
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_user_by_id(self, user_1, users_dao):
        assert users_dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self, users_dao):
        assert users_dao.get_by_id(1) is None

    def test_get_user_by_email(self, user_1, users_dao):
        assert users_dao.get_by_email("user@mail") == user_1

    def test_post_user(self, users_dao):
        data = {"email": "user@mail", "password": "Ll+ELt6teHvJetNJunNqeCXfrMFuy4axx++vThbl8V0=", "name": "user", "surname": "userss", "favorite_genre": 1}
        assert users_dao.create(data).email == "user@mail"

    def test_update_user(self, users_dao, user_1):
        user_1.name = "name"
        users_dao.update_partial(user_1)
