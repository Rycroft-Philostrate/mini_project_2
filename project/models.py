from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship


from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100))
    description = Column(String(300))
    trailer = Column(String(300))
    year = Column(Integer)
    rating = Column(Float)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    genre = relationship("Genre")
    director_id = Column(Integer, ForeignKey("directors.id"))
    director = relationship("Director")


class User(models.Base):
    __tablename__ = "users"

    email = Column(String(100), unique=True)
    password = Column(String(150))
    name = Column(String(100))
    surname = Column(String(100))
    favorite_genre = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("Genre")


class Favorite(models.Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    movie_id = Column(Integer, ForeignKey("movies.id"))
    movie = relationship("Movie")
