from flask_restful import Resource, reqparse
from models.favorite_beers import FavoriteBeersModel

_parser = reqparse.RequestParser()
_parser.add_argument('beer_id',
type=int,
required=True,
help="This field cannot be blank."
)

class FavoriteBeers(Resource):
    def post(self, user_id):
        data = _parser.parse_args()
        data.user_id = user_id

        favorite = FavoriteBeersModel(**data)

        try:
            favorite.save_to_db()
        except:
            return {"message": "An error occurred favoriting the beer."}, 500

        return favorite.json(), 201

    @classmethod
    def delete(cls, id):
        brewery = FavoriteBeersModel.find_by_id(id)
        if brewery:
            brewery.delete_from_db()

        return {'message': 'Brewery deleted'}


class FavoritesList(Resource):
    @classmethod
    def get(cls):
        return [brewery.json() for brewery in FavoriteBeersModel.find_all()]
