import pytest

from project.dao import DirectorsDAO
from project.models import Director


class TestDirectorDAO:

    @pytest.fixture
    def directors_dao(self, db):
        return DirectorsDAO(db.session)

    @pytest.fixture
    def director_1(self, db):
        g = Director(name="Питер Джексон")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def director_2(self, db):
        g = Director(name="Джеймс Кемерон")
        db.session.add(g)
        db.session.commit()
        return g

    def test_get_directors_by_id(self, director_1, directors_dao):
        assert directors_dao.get_by_id(director_1.id) == director_1

    def test_get_directors_by_id_not_found(self, directors_dao):
        assert directors_dao.get_by_id(1) is None

    def test_get_all_directors(self, director_1, director_2, directors_dao):
        assert directors_dao.get_all() == [director_1, director_2]

    def test_get_directors_by_page(self, app, directors_dao, director_1, director_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert directors_dao.get_all(page=1) == [director_1]
        assert directors_dao.get_all(page=2) == [director_2]
        assert directors_dao.get_all(page=3) == []
