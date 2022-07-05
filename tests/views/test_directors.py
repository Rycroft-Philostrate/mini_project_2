import pytest

from project.models import Director


class TestDirectorsView:
    @pytest.fixture
    def directors(self, db):
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, directors):
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json == [{"id": directors.id, "name": directors.name}]

    def test_director_pages(self, client, directors):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/directors/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_director(self, client, directors):
        response = client.get("/directors/1/")
        assert response.status_code == 200
        assert response.json == {"id": directors.id, "name": directors.name}

    def test_director_not_found(self, client, directors):
        response = client.get("/directors/2/")
        assert response.status_code == 404
