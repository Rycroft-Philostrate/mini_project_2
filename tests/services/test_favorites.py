from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import Favorite
from project.services import FavoriteService


class TestFavoritesService:

    @pytest.fixture()
    @patch('project.dao.FavoritesDAO')
    def favorites_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_favorite.return_value = Favorite(id=1, movie_id=67, user_id=3)
        dao.create.return_value = Favorite(id=2, movie_id=7, user_id=4)

        return dao

    @pytest.fixture()
    def favorites_service(self, favorites_dao_mock):
        return FavoriteService(dao=favorites_dao_mock)

    def test_create_favorite(self, favorites_service):
        favorite = favorites_service.create({"user_id": 2, "movie_id": 67})
        assert favorite.user_id == 4

    def test_delete_favorite(self, favorites_service):
        favorites_service.delete(4, 3)

    def test_delete_favorite_not_found(self, favorites_dao_mock, favorites_service):
        favorites_dao_mock.get_favorite.return_value = None

        with pytest.raises(ItemNotFound):
            favorites_service.delete(10, 11)
