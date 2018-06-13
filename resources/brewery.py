from flask_restful import Resource, reqparse
from models.brewery import BreweryModel


class Brewery(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('brewery_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('brewery_logo',
                        type=str,
                        required=True,
                        help="Every brewery needs a logo."
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="Every brewery needs an address."
                        )
    parser.add_argument('city',
                        type=str,
                        required=True,
                        help="Every brewery needs a city"
                        )
    parser.add_argument('state',
                        type=str,
                        required=True,
                        help="Every brewery needs a state"
                        )
    parser.add_argument('zip',
                        type=int,
                        required=True,
                        help="Every brewery needs a zip."
                        )
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="Every brewery needs a phone"
                        )
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help="Every brewery needs a url"
                        )

    @classmethod
    def get(cls, brewery_id:int):
        brewery = BreweryModel.find_by_id(brewery_id)
        if brewery:
            return brewery.json()
        return {'message': 'Brewery not found'}, 404

    @classmethod
    def post(cls, brewery_id:int):
        if BreweryModel.find_by_id(brewery_id):
            return {'message': "A brewery with id '{}' already exists.".format(id)}, 400

        brewery = BreweryModel(brewery_id)
        try:
            brewery.save_to_db()
        except:
            return {"message": "An error occurred creating the brewery."}, 500

        return brewery.json(), 201

    @classmethod
    def delete(cls, id):
        brewery = BreweryModel.find_by_id(id)
        if brewery:
            brewery.delete_from_db()

        return {'message': 'Brewery deleted'}


class BreweryList(Resource):
    @classmethod
    def get(cls):
        return [brewery.json() for brewery in BreweryModel.find_all()]
