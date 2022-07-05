import pytest
from unittest.mock import patch

from project.models import Favorite, User
from project.container import auth_service

class TestFavoritesView:

    @pytest.fixture
    def favorite(self, db):
        obj = Favorite(user_id=1, movie_id=67)
        db.session.add(obj)
        db.session.commit()
        return obj

    @pytest.fixture
    def user_1(self, db):
        obj = User(email="user@mail", password="UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE=", name="user_3", surname="userss_3", favorite_genre=1)
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

    def test_favorite_post(self, client, user_1, auth_token):
        response = client.post("/favorites/movies/1/", headers=auth_token)
        assert response.status_code == 201
        assert response.json == {"id": 1, "user_id": 1, "movie_id": 1}

    def test_favorite_delete(self, client, favorite, user_1, auth_token):
        with patch('project.container.user_service') as users_service_mock:
            users_service_mock.get_by_email.return_value = User(id=1, email="user@mail",
                                                                password="UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE=",
                                                                name="user", surname="userss", favorite_genre=1)
            response = client.delete("/favorites/movies/67/", headers=auth_token)
            assert response.status_code == 204
