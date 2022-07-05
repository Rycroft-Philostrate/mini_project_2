from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash, compare_password


class UserService:
	def __init__(self, dao: BaseDAO) -> None:
		self.dao = dao

	def get_item(self, pk: int) -> User:
		if user := self.dao.get_by_id(pk):
			return user
		raise ItemNotFound(f'User with pk={pk} not exists.')

	def get_by_email(self, email: str) -> User:
		if user := self.dao.get_by_email(email):
			return user
		raise ItemNotFound(f'User with email={email} not exists.')

	def create(self, user_d):
		user_d['password'] = generate_password_hash(user_d.get('password'))
		return self.dao.create(user_d)

	def update_partial(self, data, email):
		user = self.dao.get_by_email(email)
		if "name" in data:
			user.name = data.get("name")
		if "surname" in data:
			user.surname = data.get("surname")
		if "favorite_genre" in data:
			user.favorite_genre = data.get("favorite_genre")
		self.dao.update_partial(user)

	def update_password(self, data, email):
		user = self.dao.get_by_email(email)
		if not compare_password(user.password, data.get('password_1')):
			return 'Bad Password', 401
		user.password = generate_password_hash(data.get('password_2'))
		self.dao.update_partial(user)

