from db import db
from seeds.breweries import breweries

class BreweryModel(db.Model):
    __tablename__ = 'breweries'

    id = db.Column(db.Integer, default=(len(breweries) + 1), primary_key=True)
    brewery_name = db.Column(db.String(80))
    brewery_logo = db.Column(db.String(200))
    address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zip = db.Column(db.Integer())
    phone = db.Column(db.String(80))
    url = db.Column(db.String(80))

    # items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, brewery_name, brwery_logo, address, city, state, zip, phone, url):
        self.brewery_name = brewery_name
        self.brewery_logo = brewery_logo
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        self.url = url

    def json(self):
        return {
            'id': self.id,
            'brewery_name': self.brewery_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'phone': self.phone,
            'url': self.url
            # 'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_brewery_name(cls, brewery_name):
        return cls.query.filter_by(brewery_name=brewery_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
