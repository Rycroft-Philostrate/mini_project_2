from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User, Favorite


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie


class UsersDAO(BaseDAO[User]):
    __model__ = User


class FavoritesDAO(BaseDAO[Favorite]):
    __model__ = Favorite
