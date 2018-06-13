from flask_restful import Resource, reqparse
from models.reviews import ReviewsModel

_parser = reqparse.RequestParser()
_parser.add_argument('user_id',
type=int,
required=True,
help="This field cannot be blank."
)
_parser.add_argument('beer_id',
type=int,
required=True,
help="This field cannot be blank."
)
_parser.add_argument('review_title',
type=str,
required=True,
help="This field cannot be blank."
)
_parser.add_argument('review_body',
type=str,
required=True,
help="This field cannot be blank."
)
_parser.add_argument('review_img',
type=str,
required=True,
help="This field cannot be blank."
)
_parser.add_argument('rating',
type=int,
required=True,
help="This field cannot be blank."
)

class Reviews(Resource):
    def post(self):
        data = _parser.parse_args()

        review = ReviewsModel(**data)

        if ReviewsModel.find_by_user_id_and_beer_id(data['user_id'], data['beer_id']):
            print('yooo')
            return {"message": "You Have already reviewed this beer!"}, 400

        try:
            review.save_to_db()
        except:
            return {"message": "An error occurred reviewing this beer."}, 500

        return review.json(), 201

    @classmethod
    def delete(cls, id):
        review = ReviewsModel.find_by_id(id)
        if review:
            review.delete_from_db()

        return {'message': 'Review deleted'}


class ReviewsList(Resource):
    @classmethod
    def get(cls):
        return [review.json() for review in ReviewsModel.find_all()]
