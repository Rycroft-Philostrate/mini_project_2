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
        token = auth_service.create_token("user@mail", "password").get("refresh_token")
        header = {
            'Authorization': f'Bearer {token}'
        }
        return header

    def test_user(self, client, user, auth_token):
        response = client.get("/users/", headers=auth_token)
        assert response.status_code == 200
        assert response.json == {"id": user.id, "email": user.email, "password": user.password, "name": user.name, "surname": user.surname, "favorite_genre": user.favorite_genre}

    def test_user_patch(self, client, user, auth_token):
        data = {"name": "name"}
        response = client.patch("/users/", json=data, headers=auth_token)
        assert response.status_code == 204

    def test_user_put_password(self, client, user, auth_token):
        data = {"password_1": "password", "password_2": "user_2"}
        response = client.put("/users/password/", json=data, headers=auth_token)
        assert response.status_code == 204
