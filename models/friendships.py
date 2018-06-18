from db import db


class FriendshipModel(db.Model):
    __tablename__ = 'friendships'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    followee_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))


    def __init__(self, follower_id, followee_id):
        self.follower_id = follower_id
        self.followee_id = followee_id

    def json(self):
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'followee_id': self.followee_id
        }

    @classmethod
    def find_by_id(cls, follower_id):
        return cls.query.filter_by(follower_id=follower_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
