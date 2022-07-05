import pytest

from project.dao import FavoritesDAO
from project.models import Favorite


class TestFavoriteDAO:
    @pytest.fixture
    def favorites_dao(self, db):
        return FavoritesDAO(db.session)

    @pytest.fixture
    def favorite_1(self, db):
        g = Favorite(user_id=1, movie_id=67)
        db.session.add(g)
        db.session.commit()
        return g

    def test_post_favorite(self, favorites_dao):
        data = {"user_id": 2, "movie_id": 67}
        assert favorites_dao.create(data).movie_id == 67

    def test_delete_favorite(self, favorites_dao, favorite_1):
        favorites_dao.delete(favorite_1)
        assert favorites_dao.get_by_id(1) is None
