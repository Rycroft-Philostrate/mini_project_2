from flask_restx import Namespace, Resource
from flask import request, abort

from project.container import user_service, auth_service
from project.setup.api.models import user

auth_ns = Namespace("auth")


@auth_ns.route('/register/')
class AuthRegister(Resource):
	@auth_ns.marshal_with(user, code=201, description='OK')
	def post(self):
		req_json = request.json
		return user_service.create(req_json), 201


@auth_ns.route('/login/')
class AuthLogin(Resource):
	@auth_ns.response(200, "OK")
	@auth_ns.response(401, "Data user incorrect")
	def post(self):
		res = request.json
		if None in [res.get('email'), res.get('password')]:
			abort(401)
		return auth_service.create_token(email=res.get('email'), password=res.get('password')), 201

	@auth_ns.response(201, "OK")
	def put(self):
		res = request.json
		return auth_service.check_refresh_token(res.get('refresh_token')), 201
