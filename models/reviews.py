from db import db
from seeds.reviews import reviews

class ReviewsModel(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    user = db.relationship('UserModel')
    beer_id = db.Column(db.Integer, db.ForeignKey('beers.id', ondelete='SET NULL'))
    beer = db.relationship('BeerModel')
    review_title = db.Column(db.String(250))
    review_body = db.Column(db.String(250))
    review_img = db.Column(db.String(250))
    rating = db.Column(db.Integer, default=1)

    def __init__(self, user_id, beer_id, review_title, review_body, rating, review_img):
        self.user_id = user_id
        self.beer_id = beer_id
        self.review_title = review_title
        self.review_body = review_body
        self.review_img = review_img
        self.rating = rating

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'beer_id': self.beer_id,
            'review_title': self.review_title,
            'review_body': self.review_body,
            'review_img': self.review_img,
            'rating': self.rating
        }

    @classmethod
    def find_by_beer_id(cls, beer_id):
        return cls.query.filter_by(beer_id=beer_id).all()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_user_id_and_beer_id(cls, user_id, beer_id):
        return cls.query.filter_by(user_id=user_id, beer_id=beer_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
