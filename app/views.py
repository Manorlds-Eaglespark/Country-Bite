import os
import re
from flask import Flask
from flask_api import FlaskAPI
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify, make_response, json
from app.helpers.flask_imgur import Imgur
from datetime import datetime
from instance.config import app_config
from dotenv import load_dotenv
from flask_cors import CORS
from shared import db
from app.models.users import User


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMGUR_ID"] = "0c78f4c5dd9bce4"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    ma = Marshmallow(app)
    imgur_handler = Imgur(app)
    CORS(app)


    @app.route('/', methods=['GET'])
    def welcome_to_api():
        response = {"status": 200,
            "message": "Welcome To Countalk API."
                    }
        return make_response(jsonify(response)), 200


    # Auth endpoints ############################################################################################################

    @app.route('/api/v1/user/login', methods=['POST'])
    def login_user():
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                access_token = user.generate_token()
                return make_response(jsonify({"message":"You successfully logged-in.", "token": access_token.decode(), "shop_owner": user.owns_shop}))
            else:
                return make_response(jsonify({"message": "You entered a wrong password."})), 401
        else:
            return make_response(jsonify({"message": "You entered wrong credentials."})), 401

    @app.route('/api/v1/user/register', methods=['POST'])
    def register_new_user():
        name = request.data.get('name', '')
        country = request.data.get('country', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        phonenumber = request.data.get('phonenumber', '')
        user_data = {"name": name, "country": country, "email": email, "password": password, "phonenumber": phonenumber}
        validate_user_data = Register_Validation(user_data)
        is_verified = validate_user_data.check_input()
        if is_verified[0] == 200:
            user = User(user_data)
            if User.query.filter_by(email=email).first():
                return make_response(jsonify({"message":"Enter a different email address. Someone already uses that email."})), 400
            else:
                user.save()
                return make_response(jsonify(
                    {"user": user_schema.dump(user), "message": "User Successfully Registered"})), 201
        else:
            return make_response(jsonify({"message":is_verified[1]})), is_verified[0]






    return app
