import pytest

from project.dao import MoviesDAO
from project.models import Movie


class TestGenreDAO:
    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        g = Movie(title="Рокетмен", description="История ...", trailer="https://youtu..", year=2019, rating=7.3, genre_id=1, director_id=1)
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def movie_2(self, db):
        g = Movie(title="Волк", description="История ...", trailer="https://youtu..", year=2022, rating=6.9, genre_id=2, director_id=2)
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert movies_dao.get_by_id(1) is None

    def test_get_all_movies(self, movie_1, movie_2, movies_dao):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_all_movies_filters(self, app, movie_1, movie_2, movies_dao):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []
        assert movies_dao.get_all(status='new', page=1) == [movie_2]
