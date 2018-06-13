from db import db
import uuid
from seeds.users import users
from models.beer import BeerModel
from models.reviews import ReviewsModel
from models.favorite_beers import FavoriteBeersModel
from collections import Counter

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    hashedPassword = db.Column(db.String(150))
    profile_pic = db.Column(db.String(150))
    location = db.Column(db.String(80))
    bio = db.Column(db.String(80))
    beers = db.relationship('FavoriteBeersModel', lazy='dynamic')
    reviews = db.relationship('ReviewsModel', lazy='dynamic')


    def __init__(self, first_name, last_name, username, email, hashedPassword, profile_pic = 'https://image1.masterfile.com/getImage/NjUzLTAzODQzODg3ZW4uMDAwMDAwMDA=AE7cdS/653-03843887en_Masterfile.jpg', location = 'BeerLand, CA', bio = 'I like beer :)'):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.hashedPassword = hashedPassword
        self.profile_pic = profile_pic
        self.location = location
        self.bio = bio

    def json(self):
        favorites_list = FavoriteBeersModel.find_by_id(self.id)
        favorites = [BeerModel.find_by_id(beer.beer_id).json() for beer in favorites_list]

        if favorites:
            favorites_to_count = [favorite['style'] for favorite in favorites if favorite['style'].isupper()]
            c = Counter(favorites_to_count)
        else:
            c = Counter(['none'])

        reviews_list = ReviewsModel.find_by_user_id(self.id)
        reviews = [review.json() for review in reviews_list]

        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'hashedPassword': self.hashedPassword,
            'profile_pic': self.profile_pic,
            'location': self.location,
            'bio': self.bio,
            'beers': favorites,
            'reviews': reviews,
            'favorite_style': c.most_common(1)[0][0]
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
