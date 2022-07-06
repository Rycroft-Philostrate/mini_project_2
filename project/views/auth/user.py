from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user
from flask import request
from project.tools.decorators import auth_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
	@user_ns.marshal_with(user, as_list=True, code=200, description='OK')
	@auth_required
	def get(self, email):
		"""Get user"""
		return user_service.get_by_email(email)

	@user_ns.marshal_with(user, code=204, description='OK')
	@auth_required
	def patch(self, email):
		"""Update data user"""
		req_json = request.json
		user_service.update_partial(req_json, email)
		return "", 204


@user_ns.route("/password/")
class UserView(Resource):
	@user_ns.marshal_with(user, code=204, description='OK')
	@auth_required
	def put(self, email):
		"""Update password user"""
		req_json = request.json
		user_service.update_password(req_json, email)
		return "", 204
