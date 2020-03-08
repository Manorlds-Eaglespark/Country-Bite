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
from app.helpers.validations import Register_Validation
from app.helpers.check_loggedin import login_required
from app.models.users import User, user_schema, users_schema
from app.models.posts import Post, post_schema, posts_schema


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
                return make_response(jsonify({"message":"You successfully logged-in.", "token": access_token.decode(), "country": user.country}))
            else:
                return make_response(jsonify({"error": "You entered a wrong password."})), 401
        else:
            return make_response(jsonify({"error": "You entered wrong credentials."})), 401

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
        if User.query.filter_by(email=email).first():
            return make_response(jsonify({"error":"Someone already uses that email. Try again with a different Email"})), 400
        if is_verified[0] == 1:
            user = User(user_data)
            user.save()
            return make_response(jsonify(
                    {"user": user_schema.dump(user), "message": "Success, Log in now"})), 201
        else:
            return make_response(jsonify({"error":is_verified[1]})), is_verified[0]



    # Post endpoints ############################################################################################################

    @app.route('/api/v1/posts', methods=['POST'])
    @login_required
    def user_add_new_post(current_user, country):
        message = request.form.get('message', '')
        image = request.files.get('image', '')
        if image:
            image_data = imgur_handler.send_image(image)
            image_url = image_data["data"]["link"]
            image_delete_hash =  image_data["data"]["deletehash"]
        else:
            image_url = ''
            image_delete_hash = ''
        post_data = {"country": country, "message": message, "image_url": image_url, "image_delete_hash": image_delete_hash, "posted_by": current_user}
        post = Post(post_data)
        post.save()
        return make_response(jsonify({'post': post_schema.dump(post), 'message': 'new post successfully successfully saved.'})), 201
        
    @app.route('/api/v1/posts/country', methods=['GET'])
    @login_required
    def user_view_country_posts(current_user, country):
        country_posts = Post.query.filter_by(country=country)
        return posts_schema.dumps(country_posts)

    @app.route('/api/v1/posts/country/<post_id>', methods=['GET', 'PUT', 'DELETE'])
    @login_required
    def user_post_edit(current_user, country, post_id):
        post = Post.query.get(post_id)
        if post:
            if request.method == 'GET':
                _post = post_schema.dumps(post)
                return make_response(jsonify({"post": _post}))
            if request.method == 'PUT':
                message = request.form.get('message', '')
                if message:
                    post.add_added(message)
                    post.save()
                    return make_response(jsonify({"message": "Post successfully updated."}))
                else:
                    return make_response(jsonify({"error":"Add the message to edit."}))

            if request.method == 'DELETE':
                post.delete()
                return make_response(jsonify({"message": "post successfully deleted."}))
        else:
            return make_response(jsonify({"error": "Resource not found."})), 404


    return app
