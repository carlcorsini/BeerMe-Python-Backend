from db import db
from seeds.breweries import breweries
import datetime

class BreweryModel(db.Model):
    __tablename__ = 'breweries'

    id = db.Column(db.Integer, primary_key=True)
    brewery_name = db.Column(db.String(80))
    brewery_logo = db.Column(db.String(200))
    address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip = db.Column(db.Integer())
    phone = db.Column(db.String(80))
    url = db.Column(db.String(80))
    beers = db.relationship('BeerModel', lazy='dynamic')
    created_at= db.Column(db.String, default=datetime.datetime.now())
    updated_at= db.Column(db.String, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __init__(self, brewery_name, brewery_logo, address, city, state, zip, phone, url):
        self.brewery_name = brewery_name
        self.brewery_logo = brewery_logo
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        self.url = url
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self):
        return {
            'id': self.id,
            'brewery_name': self.brewery_name,
            'brewery_logo': self.brewery_logo,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'phone': self.phone,
            'url': self.url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'beers': [beer.json() for beer in self.beers.all()]
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
