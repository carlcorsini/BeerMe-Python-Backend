from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()
    db.engine.execute(UserModel.__table__.insert(), users)
    db.engine.execute(BeerModel.__table__.insert(), beers)
    db.engine.execute(BreweryModel.__table__.insert(), breweries)
