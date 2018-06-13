from db import db
from seeds.favorite_beers import favorite_beers

class FavoriteBeersModel(db.Model):
    __tablename__ = 'favorite_beers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    user = db.relationship('UserModel')
    beer_id = db.Column(db.Integer, db.ForeignKey('beers.id', ondelete='SET NULL'))
    beer = db.relationship('BeerModel')

    def __init__(self, user_id, beer_id):
        self.user_id = user_id
        self.beer_id = beer_id

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'beer_id': self.beer_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(user_id=_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
