from project.dao import GenresDAO, DirectorsDAO, MoviesDAO, UsersDAO, FavoritesDAO

from project.services import GenresService, DirectorsService, MoviesService, UserService, AuthService, FavoriteService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UsersDAO(db.session)
favorite_dao = FavoritesDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UserService(dao=user_dao)
favorite_service = FavoriteService(dao=favorite_dao)
auth_service = AuthService(user_service=user_service)
