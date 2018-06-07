from db import db
from seeds.beers import beers

class BeerModel(db.Model):
    __tablename__ = 'beers'

    id = db.Column(db.Integer, default=(len(beers) + 1), primary_key=True)
    beer_name = db.Column(db.String(80))
    style = db.Column(db.String(80))
    abv = db.Column(db.Float(precision=2))
    ibu = db.Column(db.Float(precision=2))
    description = db.Column(db.String(1000))
    beer_label = db.Column(db.String(250))
    # store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # store = db.relationship('StoreModel')

    def __init__(self, beer_name, style, store_id):
        self.beer_name = beer_name
        self.style = style
        self.abv = abv
        self.ibu = ibu
        self.description = description
        self.beer_label = beer_label
        # self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'beer_name': self.beer_name,
            'style': self.style,
            'abv': self.abv,
            'ibu': self.ibu,
            'description': self.description,
            'beer_label': self.beer_label
            # 'store_id': self.store_id
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
