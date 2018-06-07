from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from models.beer import BeerModel


class Beer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('beer_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('style',
                        type=str,
                        required=True,
                        help="Every beer needs a style."
                        )
    parser.add_argument('abv',
                        type=float,
                        required=True,
                        help="Every beer needs an ABV."
                        )
    parser.add_argument('ibu',
                        type=int,
                        required=False
                        )
    parser.add_argument('description',
                        type=str,
                        required=False
                        )
    parser.add_argument('beer_label',
                        type=str,
                        required=True,
                        help="Every beer needs a beer_label."
                        )

    @jwt_required
    def get(self, beer_id: int):
        beer = BeerModel.find_by_id(beer_id)
        if beer:
            return beer.json()
        return {'message': 'Beer not found'}, 404

    @fresh_jwt_required
    def post(self, beer_name):
        if BeerModel.find_by_name(beer_name):
            return {'message': "An beer with beer_name '{}' already exists.".format(beer_name)}, 400

        data = self.parser.parse_args()

        beer = BeerModel(beer_name, **data)

        try:
            beer.save_to_db()
        except:
            return {"message": "An error occurred while inserting the beer."}, 500

        return beer.json(), 201

    @jwt_required
    def delete(self, beer_name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        beer = BeerModel.find_by_name(beer_name)
        if beer:
            beer.delete_from_db()
            return {'message': 'Beer deleted.'}
        return {'message': 'Beer not found.'}, 404

    def put(self, beer_name):
        data = self.parser.parse_args()

        beer = BeerModel.find_by_name(beer_name)

        if beer:
            beer.price = data['price']
        else:
            beer = BeerModel(beer_name, **data)

        beer.save_to_db()

        return beer.json()


class BeerList(Resource):
    # @jwt_optional
    def get(self):
        # user_id = get_jwt_identity()
        beers = [beer.json() for beer in BeerModel.find_all()]
        # if user_id:
        return {'beers': beers}, 200
        # return {
        #     'beers': [beer['beer_name'] for beer in beers],
        #     'message': 'More data available if you log in.'
        # }, 200
