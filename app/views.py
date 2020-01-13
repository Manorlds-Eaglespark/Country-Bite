import os
from flask_api import FlaskAPI
from flask import make_response, request, jsonify, json
from flask_cors import CORS 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from instance.config import app_config
from shared import db, ma
from app.models.users import User, users_schema, user_schema
from app.models.countries import Country, country_schema, countries_schema
from app.models.posts import Post, post_schema, posts_schema
from app.utilities.model_validations import Register_Validation
from app.utilities.login_requirements import login_required
                

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    ma = Marshmallow(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def welcome_to_api():
        """Check if API is running"""
        response = {"status": 200,
            "message": "Welcome To Country Bite App Backend API"}
        return make_response(jsonify(response)), 200

    
########################################################################################### Login & Register

    @app.route('/api/v1/user/register', methods=['POST'])
    def register_new_user():
        name = request.get_json()['name']
        country = request.get_json()['country']
        phone = request.get_json()['phone']
        password = request.get_json()['password']
        email = request.get_json()['email']
        role = request.get_json()['role']
        thumbnail = request.get_json()['thumbnail'] 
        if not thumbnail: 
            thumbnail = 'https://img.favpng.com/20/11/12/computer-icons-user-profile-png-favpng-0UAKKCpRRsMj5NaiELzw1pV7L.jpg'
        verify_data = Register_Validation({"name":name, "country": country, "password":password, "email":email, "thumbnail":thumbnail, "role":role})
        is_verified = verify_data.check_input()
        if is_verified[0] == 200:
            if not User.query.filter_by(email=email).first():
                new_user = User(name, country, password, phone, email, thumbnail, role)
                new_user.save()
                return make_response(jsonify({"message": "User successfully created!"})), 201
            else:
                return make_response(jsonify({"message": "Email already being used here."}))   
        else:
            return make_response(jsonify({"message":is_verified[1]})), is_verified[0]

    @app.route('/api/v1/user/login', methods=['POST'])
    def login_registered_user():
        email = request.get_json()['email']
        password = request.get_json()['password']
        user = User.query.filter_by(email=email).first()
        if user: 
            if user.user_email_verified(password):
                token = user.generate_token()
                return user.login_times + ""
                user.last_login = datetime.now()
                user.save()
                return make_response(jsonify({"token": token, "message": "You have successfully LoggedIn"})),200
            else:
                return make_response(jsonify({"message": "You entered a wrong password"})),200
        else:
            return make_response(jsonify({"message": "Wrong credentials, try again"})),200


########################################################################################### Countries CRUD

    @app.route('/api/v1/countries', methods=['GET','POST'])
    @login_required
    def get_add_new_country(current_user, user_country):
        if request.method == 'GET':
            countries = Country.query.all()
            return make_response(jsonify({"countries": countries_schema.dump(countries)})), 200
        if request.method == 'POST':
            name =   request.data.get('name', '')
            code =  request.data.get('code', '')
            if name and code:
                new_country = Country(name, code)
                new_country.save()
                return make_response(jsonify({"message": "Country successfully saved!", "country": country_schema.dump(new_country)})), 201
            else:
                return make_response(jsonify({"message": "Add a country name and code"})), 400

    @app.route('/api/v1/countries/<country_id>', methods=['GET','PUT','DELETE'])
    @login_required
    def get_update_delete_country(current_user, user_country, id):
        country = Country.query.get(id)
        if country:
            if request.method == 'DELETE':
                country.delete()
                return make_response(jsonify({"message": "You Successfully deleted Country "+id})), 202
            elif request.method == 'GET':
                return make_response(jsonify({"country": country_schema.dump(country)})), 200
            elif request.method == 'PUT':
                name = str(request.data.get('name', ''))
                code = int(request.data.get('code', 0))
                if name and code:
                    country.name = name
                    country.code = code
                    country.save()
                    return make_response(jsonify({"message":"You successfully updated country "+id, "country": country_schema.dump(country)})), 202
                else:
                    return make_response(jsonify({"message":"Include both Name & Code"})), 400
        else:
            return make_response(jsonify({"message": "Country does not exist"})), 404


########################################################################################### Posts CRUD

    @app.route('/api/v1/posts', methods=['GET','POST'])
    @login_required
    def get_add_new_post(current_user, user_country):
        if request.method == 'GET':
            posts = Post.query.all()
            return make_response(jsonify({"posts": posts_schema.dump(posts)})), 200
        if request.method == 'POST':
            user =   current_user
            country =   Country.query.filter_by(name=user_country).first()
            message =  request.data.get('message', '')
            image =   request.data.get('image','')
           
            if message or image == 200:
                new_post = Post(user, country.id, message, image)
                new_post.save()
                return make_response(jsonify({"message": "Post successfully saved!", "Post": post_schema.dump(new_post)})), 201
            else:
                return make_response(jsonify({"message": "Add some text or upload image"})), 400


    @app.route('/api/v1/posts/<post_id>', methods=['GET','PUT','DELETE'])
    @login_required
    def get_update_delete_posts(current_user, user_country, post_id):
        post = Post.query.get(post_id)
        if post:
            if request.method == 'DELETE':
                post.delete()
                return make_response(jsonify({"message": "You Successfully deleted Post "+id})), 202
            elif request.method == 'GET':
                return make_response(jsonify({"post": post_schema.dump(post)})), 200
            elif request.method == 'PUT':
                message =   str(request.data.get('message', ''))
                image =  str(request.data.get('image', ''))
                if current_user == post.user and user_country == post.country:
                    if message:
                        post.message = message
                    if image:
                        post.image = image
                    post.save()
                    return make_response(jsonify({"message":"You successfully updated post "+id, "review": post_schema.dump(post)})), 202
                else:
                    return make_response(jsonify({"message":"This Post belongs to a different user"})), 400
        else:
            return make_response(jsonify({"message": "Post does not exist"})), 404

    return app