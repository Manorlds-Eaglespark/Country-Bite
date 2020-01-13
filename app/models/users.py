import os
import jwt
from flask_bcrypt import Bcrypt
from shared import ma
from app.views import db
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155))
    country = db.Column(db.String(255))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(255))
    thumbnail = db.Column(db.String(255))
    role = db.Column(db.String(20))
    time_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime)
    login_times = db.Column(db.Integer)

    def __init__(self, name, country, password, phone, email, thumbnail, role):
        self.name = name
        self.country = country
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.phone = phone
        self.email = email
        self.thumbnail = thumbnail
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def user_email_verified(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self):
        """ Generates the access token """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=300),
                'iat': datetime.utcnow(),
                'sub': self.id,
                'rle': self.role,
                'country': self.country
            }
            jwt_string = jwt.encode(
                payload,
                str(os.getenv('SECRET')),
                algorithm='HS256'
            )
            return jwt_string.decode()

        except Exception as e:
            return str(e)

    def decode_token(self, token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, str(os.getenv('SECRET')))
            return [payload['sub'], payload['country']]
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

class UserSchema(ma.Schema):
    class Meta:
        fields = ("name", "email", "thumbnail", "role", "time_added")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
