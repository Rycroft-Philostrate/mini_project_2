import pytest

from project.models import Movie


class TestMoviesView:
    @pytest.fixture
    def movie(self, db):
        obj = Movie(title="Волк", description="История ...", trailer="https://youtu..", year=2022, rating=6.9, genre_id=2, director_id=2)
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, movie):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json == [{"id": movie.id, "title": movie.title, "description": movie.description, "trailer": movie.trailer, "year": movie.year, "rating": movie.rating, "genre_id": movie.genre_id, "director_id": movie.director_id}]

    def test_movie_pages(self, client, movie):
        response = client.get("/movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/movies/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

        response = client.get("/movies/?status = new&page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_movie(self, client, movie):
        response = client.get("/movies/1/")
        assert response.status_code == 200
        assert "title" in response.json

    def test_movie_not_found(self, client, movie):
        response = client.get("/movies/2/")
        assert response.status_code == 404
