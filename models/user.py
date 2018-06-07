from db import db
from seeds.users import users

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, default=(len(users)+ 1), primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    hashedPassword = db.Column(db.String(80))
    profile_pic = db.Column(db.String(150))
    location = db.Column(db.String(80))
    bio = db.Column(db.String(80))

    def __init__(self, first_name, last_name, username, email, hashedPassword, profile_pic, location, bio):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.hashedPassword = hashedPassword
        self.profile_pic = profile_pic
        self.location = location
        self.bio = bio

    def json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'hashedPassword': self.hashedPassword,
            'profile_pic': self.profile_pic,
            'location': self.location,
            'bio': self.bio
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
