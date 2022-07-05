from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Favorite


class FavoriteService:
	def __init__(self, dao: BaseDAO) -> None:
		self.dao = dao

	def create(self, data) -> Favorite:
		return self.dao.create(data)

	def delete(self, movie_id, user_id):
		if favorite := self.dao.get_favorite(movie_id, user_id):
			self.dao.delete(favorite)
		else:
			raise ItemNotFound(f'Favorite with {movie_id} and {user_id} not exists.')
