import pytest

from project.models import User
from project.container import auth_service


class TestUsersView:

    @pytest.fixture
    def user(self, db):
        obj = User(email="user@mail", password="UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE=", name="user", surname="userss", favorite_genre=1)
        db.session.add(obj)
        db.session.commit()
        return obj

    @pytest.fixture
    def auth_token(self):
        token = auth_service.create_token("user@mail", "password")
        return token

    def test_auth_register(self, client, user):
        data = {"email": "name", "password": "password"}
        response = client.post("/auth/register/", json=data)
        assert response.status_code == 201
        assert "email" in response.json

    def test_auth_login_post(self, client, user):
        data = {"email": "user@mail", "password": "password"}
        response = client.post("/auth/login/", json=data)
        assert response.status_code == 201
        assert "access_token" in response.json

    def test_auth_login_put(self, client, user, auth_token):
        data = {'access_token': f'{auth_token.get("access_token")}',
                'refresh_token': f'{auth_token.get("refresh_token")}'}
        response = client.put("/auth/login/", json=data)
        assert response.status_code == 201
        assert "access_token" in response.json
