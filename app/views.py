import os
from flask_api import FlaskAPI
from flask import make_response, request, jsonify, json
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from instance.config import app_config
from shared import db, ma
from app.models.user import User
from app.models.categories import Category, categories_schema, category_schema
from app.models.agents import Agent, agents_schema, agent_schema
from app.models.properties import Property, properties_schema, property_schema
from app.models.reviews import  Review, review_schema, reviews_schema
from app.models.locations import Location, location_schema, locations_schema
from app.models.amenities import Amenity, amenities_schema, amenity_schema
from app.models.photos import Photo, photo_schema, photos_schema
from app.utilities.user_functions import User_Functions
from app.utilities.model_validations import Register_Validation, Amenity_Validation, \
    Category_Validation, Agent_Validation, Location_Validation, Photo_Validation, \
        Property_Validation, Review_Validation
from app.utilities.login_requirements import login_required
from app.utilities.helpers import Helpers
                

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    ma = Marshmallow(app)
    helper = Helpers()
    CORS(app)

    @app.route('/', methods=['GET'])
    def welcome_to_api():
        """Check if API is running"""
        response = {"status": 200,
            "message": "Welcome To Country Bite App Backend API"}
        return make_response(jsonify(response)), 200


    return app