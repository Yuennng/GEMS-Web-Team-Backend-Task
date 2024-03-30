from . import db, ma
from flask_login import UserMixin


class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invite_id = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    invitee = db.Column(db.Boolean)
    invite_id = db.Column(db.String(150), nullable=True)
    name = db.Column(db.String(150), nullable=True)
    email1 = db.Column(db.String(150), unique=True)
    email2 = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(150), nullable=True)
    phone_num = db.Column(db.String(150), nullable=True)
    org_name = db.Column(db.String(150), nullable=True)
    org_role = db.Column(db.String(150), nullable=True)
    valid_date = db.Column(db.String(150), nullable=True)
    profile_pic = db.Column(db.String(), nullable=True)
    invitations = db.relationship('Invitation')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'invitee', 'invite_id', 'name', 'email1', 'email2',
                   'password', 'phone_num', 'org_name', 'org_role', 'valid_date', 'profile_pic')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

