import os

from flask_cors import CORS
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.beer import Beer, BeerList
from resources.brewery import Brewery, BreweryList
from resources.favorite_beers import FavoriteBeers
from resources.reviews import Reviews

from models.user import UserModel
from models.beer import BeerModel
from models.brewery import BreweryModel
from models.favorite_beers import FavoriteBeersModel
from models.reviews import ReviewsModel
from models.friendships import FriendshipModel

from seeds.users import users
from seeds.beers import beers
from seeds.breweries import breweries
from seeds.favorite_beers import favorite_beers
from seeds.reviews import reviews
from seeds.friendships import friendships

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://carlcorsini:postgres@localhost/beer-me-python')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


app.config['JWT_SECRET_KEY'] = 'jose'  # we can also use app.secret like before, Flask-JWT-Extended can recognize both
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

# JWT configuration ends


# @app.before_first_request
# def create_tables():
#     db.drop_all()
#     db.create_all()
#     db.engine.execute(UserModel.__table__.insert(), users)
#     db.engine.execute(BreweryModel.__table__.insert(), breweries)
#     db.engine.execute(BeerModel.__table__.insert(), beers)
#     db.engine.execute(FavoriteBeersModel.__table__.insert(), favorite_beers)
#     db.engine.execute(ReviewsModel.__table__.insert(), reviews)
#     db.engine.execute(FriendshipModel.__table__.insert(), friendships)

api.add_resource(Brewery, '/breweries/<int:brewery_id>')
api.add_resource(BreweryList, '/breweries')
api.add_resource(Beer, '/beers/<int:beer_id>')
api.add_resource(BeerList, '/beers')
api.add_resource(FavoriteBeers, '/user/<int:user_id>/beers')
api.add_resource(Reviews, '/reviews')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/token')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
