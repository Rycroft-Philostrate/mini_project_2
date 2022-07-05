from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Тейлор Шеридан'),
})

movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Йеллоустоун'),
    'description': fields.String(required=True, max_length=300, example='Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»'),
    'trailer': fields.String(required=True, max_length=300, example='https://www.youtube.com/watch?v=UKei_d0cbP4'),
    'year': fields.Integer(required=True, example=2018),
    'rating': fields.Float(required=True, example=8.6),
    'genre_id': fields.Integer(required=True, example=17),
    'director_id': fields.Integer(required=True, example=1),
})

user: Model = api.model('Пользователь', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='user@mail'),
    'password': fields.String(required=True, max_length=150, example='iausd48weh342'),
    'name': fields.String(required=True, max_length=100, example='name'),
    'surname': fields.String(required=True, max_length=100, example='userss'),
    'favorite_genre': fields.Integer(required=True, example=1),
})

favorite: Model = api.model('Избранное', {
    'id': fields.Integer(required=True, example=1),
    'user_id': fields.Integer(required=True, example=1),
    'movie_id': fields.Integer(required=True, example=4),
})
