from flask import request, abort, current_app
import jwt


def auth_required(func):
	"""Проверка авторизации пользователя"""
	def wrapper(*args, **kwargs):
		if 'Authorization' not in request.headers:
			abort(401)
		token = request.headers.get('Authorization').split()[-1]
		try:
			user = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
			email = user.get('email')
		except Exception as e:
			print(f'Token decode Exception {e}')
			abort(401)
		return func(email=email, *args, **kwargs)
	return wrapper
