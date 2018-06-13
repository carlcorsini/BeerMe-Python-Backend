from db import db
from seeds.beers import beers
from models.reviews import ReviewsModel
import datetime

class BeerModel(db.Model):
    __tablename__ = 'beers'

    id = db.Column(db.Integer, primary_key=True)
    beer_name = db.Column(db.String(80))
    style = db.Column(db.String(80))
    abv = db.Column(db.Float(precision=2))
    ibu = db.Column(db.Float(precision=2))
    description = db.Column(db.String(1000))
    beer_label = db.Column(db.String(250))
    brewery_id = db.Column(db.Integer, db.ForeignKey('breweries.id', ondelete='SET NULL'))
    brewery = db.relationship('BreweryModel')
    reviews = db.relationship('ReviewsModel', lazy='dynamic')
    averageRating = db.Column(db.Integer)
    created_at = db.Column(db.String, default=datetime.datetime.now())
    updated_at = db.Column(db.String, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __init__(self, beer_name, style, abv, ibu, brewery_id, beer_label, description = 'none'):
        self.beer_name = beer_name
        self.style = style
        self.abv = abv
        self.ibu = ibu
        self.description = description
        self.beer_label = beer_label
        self.brewery_id = brewery_id

    @classmethod
    def average_rating(cls, ratings):
        try:
            return sum(ratings)/len(ratings)
        except ZeroDivisionError:
            return 0

    def json(self):
        review_list = ReviewsModel.find_by_beer_id(self.id)
        reviews = [review.json() for review in review_list]
        ratings = [review['rating'] for review in reviews]
        average = self.average_rating(ratings)

        return {
            'id': self.id,
            'beer_name': self.beer_name,
            'style': self.style,
            'abv': self.abv,
            'ibu': self.ibu,
            'description': self.description,
            'beer_label': self.beer_label,
            'brewery_id': self.brewery_id,
            'reviews': reviews,
            'average_rating': average
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, beer_name):
        return cls.query.filter_by(beer_name=beer_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
