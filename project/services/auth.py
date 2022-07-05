import calendar

from project.tools.security import compare_password
from project.services import UserService
from datetime import datetime, timedelta
from flask import current_app
from project.setup.db import db
import jwt


class AuthService:
	def __init__(self, user_service: UserService(db.session)):
		self.user_service = user_service

	def create_token(self, email, password, check_refresh=False):
		user = self.user_service.get_by_email(email)
		if user is None:
			return 'Bad Email', 401
		if not check_refresh:
			if not compare_password(user.password, password):
				return 'Bad Password', 401
		min30 = datetime.utcnow() + timedelta(minutes=30)
		data = {'email': user.email, 'exp': calendar.timegm(min30.timetuple())}
		access_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
		days30 = datetime.utcnow() + timedelta(days=30)
		data = {'email': user.email, 'exp': calendar.timegm(days30.timetuple())}
		refresh_token = jwt.encode(data, current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
		return {'access_token': access_token, 'refresh_token': refresh_token}

	def check_refresh_token(self, refresh_token):
		data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
		email = data.get('email')
		exp = data.get('exp')
		user = self.user_service.get_by_email(email)
		if user is None:
			return 'Bad Token', 401
		if not datetime.fromtimestamp(exp) >= datetime.utcnow():
			return 'Bad Token', 401
		return self.create_token(user.email, user.password, check_refresh=True)
