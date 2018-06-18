from app import app
from db import db
from models.user import UserModel
from models.beer import BeerModel
from models.brewery import BreweryModel
from models.reviews import ReviewsModel
from seeds.users import users
from seeds.beers import beers
from seeds.breweries import breweries
from seeds.favorite_beers import favorite_beers
from seeds.reviews import reviews

db.init_app(app)

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()
    db.engine.execute(UserModel.__table__.insert(), users)
    db.engine.execute(BreweryModel.__table__.insert(), breweries)
    db.engine.execute(BeerModel.__table__.insert(), beers)
    db.engine.execute(ReviewsModel.__table__.insert(), favorite_beers)
    db.engine.execute(ReviewsModel.__table__.insert(), reviews)
