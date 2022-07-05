from flask_restx import Namespace, Resource

from project.container import favorite_service, user_service
from project.setup.api.models import favorite
from project.tools.decorators import auth_required


favorites_ns = Namespace("favorites")


@favorites_ns.route("/movies/<int:movie_id>/")
@favorites_ns.param("movie_id", "ID movie")
class FavoritesView(Resource):
    @favorites_ns.expect(favorite)
    @favorites_ns.response(404, 'Not Found')
    @favorites_ns.marshal_with(favorite, code=201, description='OK')
    @auth_required
    def post(self, movie_id, email):
        """Add movie in favorites"""
        user_id = user_service.get_by_email(email).id
        data = {'movie_id': movie_id, 'user_id': user_id}
        return favorite_service.create(data), 201

    @favorites_ns.expect(favorite)
    @favorites_ns.marshal_with(favorite, code=204, description='OK')
    @auth_required
    def delete(self, movie_id, email):
        """Delete movie in favorites"""
        user_id = user_service.get_by_email(email).id
        favorite_service.delete(movie_id, user_id)
        return "", 204
