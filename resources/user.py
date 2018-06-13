from flask_restful import Resource, reqparse
import bcrypt
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

from blacklist import BLACKLIST
from models.user import UserModel

_register_parser = reqparse.RequestParser()
_register_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_register_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_register_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_register_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_register_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_login_parser = reqparse.RequestParser()
_login_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_login_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_edit_parser = reqparse.RequestParser()
_edit_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_edit_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_edit_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_edit_parser.add_argument('location',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_edit_parser.add_argument('bio',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):
    def post(self):
        data = _register_parser.parse_args()
        hashedPassword = bcrypt.hashpw(data.password.encode('utf8'), bcrypt.gensalt(10))
        data.hashedPassword = hashedPassword.decode('utf8')
        data.pop('password', 0)
        print(hashedPassword)
        print(data)
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400
        user = UserModel(**data)
        print(user)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    def post(self):
        data = _login_parser.parse_args()

        user = UserModel.find_by_email(data['email'])
        print(user)
        if user and bcrypt.checkpw(data['password'].encode('utf8'), user.hashedPassword.encode('utf8')):
            token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'token': token,
                       'refresh_token': refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    def put(cls, user_id: int):
        data = _edit_parser.parse_args()
        user = UserModel.find_by_id(user_id)

        userJSON = user.json()
        data['email'] = userJSON['email']
        data['hashedPassword'] = userJSON['hashedPassword']
        data['profile_pic'] = userJSON['profile_pic']
        updated_user = UserModel(**data)
        
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']
        user.location = data['location']
        user.bio = data['bio']
        user.save_to_db()


        return updated_user.json(), 200


    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
