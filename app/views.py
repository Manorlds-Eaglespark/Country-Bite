import os
import re
from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required)
from flask_api import FlaskAPI
from flask_bcrypt import Bcrypt
from google.oauth2 import id_token
from google.auth.transport import requests 
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify, make_response, json
from app.helpers.flask_imgur import Imgur
from datetime import datetime, timedelta
from instance.config import app_config
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import timedelta
from shared import db
from app.models.users import User
from app.helpers.validations import Register_Validation, get_country_detail
from app.models.users import User, user_schema, users_schema
from app.models.posts import Post, post_schema, posts_schema
from app.models.comments import Comment, comment_schema, comments_schema
from app.models.likes import Like, like_schema, likes_schema
from app.models.bookmarks import Bookmark, bookmark_schema, bookmarks_schema
from app.models.feedback import Feedback, feedback_schema, feedbacks_schema
from app.models.images import PhotoImage, photoimage_schema, photoimages_schema
from app.helpers.validations import allowed_file

POSTS_PER_PAGE = 15

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMGUR_ID"] = os.getenv('IMGSER')
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    db.init_app(app)
    ma = Marshmallow(app)
    imgur_handler = Imgur(app)
    jwt = JWTManager(app)
    CORS(app)


    @app.route('/', methods=['GET'])
    def welcome_to_api():
        response = {"status": 200, "message": "Welcome To Countalk API."}
        return make_response(jsonify(response)), 200


    # Auth endpoints ############################################################################################################

    @app.route('/api/v1/user/login', methods=['POST'])
    def login_user():
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                country = get_country_detail(user.country)
                access_token = create_access_token(identity={'id': user.id, 'country': country['id']}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": country}))
            else:
                return make_response(jsonify({"error": "You entered a incorrect password."})), 401
        else:
            return make_response(jsonify({"error": "Incorrect credentials."})), 401


    @app.route('/api/v1/user/register', methods=['POST'])
    def register_new_user():
        name = request.data.get('name', '')
        country = request.data.get('country', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        phonenumber = request.data.get('phonenumber', '')
        about = "I love Countalk very much."
        user_data = {"name": name, "country": country, "email": email, "about": about, "password": password, "phonenumber": phonenumber}
        validate_user_data = Register_Validation(user_data)
        is_verified = validate_user_data.check_input()
        if User.query.filter_by(email=email).first():
            return make_response(jsonify({"error":"Email address already used."})), 400
        if is_verified[0] == 1:
            user = User(user_data)
            user.save()
            return make_response(jsonify(
                    {"user": user_schema.dump(user), "message": "Success, Log in now"})), 201
        else:
            return make_response(jsonify({"error":is_verified[1]})), is_verified[0]

       
    @app.route('/api/v1/user/login/social', methods=['POST'])
    def login_social_user():
        provider = request.data.get('provider', '')
        authToken = request.data.get('token','')

        if(provider == 'Google'):
            id_info = id_token.verify_oauth2_token(authToken, requests.Request(), os.getenv('CLIENT_ID'))
            if id_info['iss'] != 'accounts.google.com':
                return make_response(jsonify({"error": "Use correct signin options."})), 401
            user =  User.query.filter_by(email=id_info['email']).first()
            
            if user:
                access_token = create_access_token(identity={'id': user.id, 'country': user.country}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": get_country_detail(user.country)}))
            else:
                return make_response(jsonify({"error":"Sign-up first to continue."}))
        
        if(provider == 'Facebook'):
            user =  User.query.filter_by(email=authToken['email']).first()
            
            if user:
                access_token = create_access_token(identity={'id': user.id, 'country': user.country}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": get_country_detail(user.country)}))
            else:
                return make_response(jsonify({"error":"Sign-up first to continue."}))



    
    @app.route('/api/v1/user/register/social', methods=['POST'])
    def register_social_user():
        provider = request.data.get('provider', '')
        country = request.data.get('country', '')
        authToken = request.data.get('token','')

        if provider == 'Google':
            id_info = id_token.verify_oauth2_token(authToken, requests.Request(), os.getenv('CLIENT_ID'))
            if id_info['iss'] != 'accounts.google.com':
                return make_response(jsonify({"error": "Use correct signin options."})), 401
            user =  User.query.filter_by(email=id_info['email']).first()
            
            if user:
                access_token = create_access_token(identity={'id': user.id, 'country': user.country}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": get_country_detail(user.country)}))
            else:
                userData = {"name": id_info['name'], "country": country, "email": id_info['email'], "about": 'I love Countalk', "password": Bcrypt().generate_password_hash('uCXyJ:%N%5Dc-K+').decode(), "phonenumber": ''}
                user = User(userData)
                user.add_image(id_info['picture'])
                user.save()
                access_token = create_access_token(identity={'id': user.id, 'country': country}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": get_country_detail(country)}))

        if provider == 'Facebook':
            user =  User.query.filter_by(email=authToken['email']).first()
            if user:
                access_token = create_access_token(identity={'id': user.id, 'country': user.country}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": get_country_detail(user.country)}))
            else:
                userData = {"name": authToken['name'], "country": country, "email": authToken['email'], "about": 'I love Countalk', "password": Bcrypt().generate_password_hash('uCXyJ:%N%5Dc-K+').decode(), "phonenumber": ''}
                user = User(userData)
                user.add_image(authToken['picture']['data']['url'])
                user.save()
                access_token = create_access_token(identity={'id': user.id, 'country': country}, expires_delta=timedelta(days=365))
                return make_response(jsonify({"message":"Successfully logged-in.", "token": access_token, "country": get_country_detail(country)}))



    # User endpoints ############################################################################################################

    @app.route('/api/v1/user', methods=['GET'])
    @jwt_required
    def get_user():
        current_user = get_jwt_identity()
        user = user_schema.dump(User.query.get(current_user['id']))
        user['country'] = get_country_detail(current_user['country'])
        rating = feedbacks_schema.dump(Feedback.query.filter_by(by=current_user['id']))
        if rating:
            user['rating'] = (rating[-1])['rating']
        else:
            user['rating'] = 0
        return make_response(jsonify({"user": user}))

    @app.route('/api/v1/user/edit', methods=['PUT'])
    @jwt_required
    def edit_user_detail():
        name = request.form.get('name','')
        about = request.form.get('about', '')
        email = request.form.get('email', '')
        profile_image = request.files.get('profile_image','')
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if user.img_del_hash and profile_image:
            imgur_handler.delete_image(delete_hash=user.img_del_hash)
        if profile_image:
            image_data = imgur_handler.send_image(profile_image)
            image_url = image_data["data"]["link"]
            image_delete_hash =  image_data["data"]["deletehash"]
            user.profile_img = image_url
            user.img_del_hash = image_delete_hash
        user.add_added({"name": name, "about": about, "email": email})
        user.save()
        return make_response(jsonify({"message":"User details successfully updated.", "user": user_schema.dump(user)})), 202


    @app.route('/api/v1/user/delete', methods=['DELETE'])
    @jwt_required
    def delete_user():
        current_user = get_jwt_identity()
        user = User.query.get(current_user['id'])
        if user:
            user.delete()
            return make_response(jsonify({"message":"User deleted."})), 200
        else:
            return make_response(jsonify({"message":"User does not exit."})), 400

                

    # Post endpoints ############################################################################################################

    @app.route('/api/v1/posts', methods=['POST'])
    @jwt_required
    def user_add_new_post():
        message = request.form.get('message', '')
        time_posted = request.form.get('time_posted', '')
        print(time_posted)
        tags = request.form.get('tags', '')
        images_number = request.form.get('images_number')
        current_user = get_jwt_identity()
        post_data = {"country": current_user['country'], "message": message, "time_posted": time_posted, "tags": tags, "posted_by": current_user['id']}
        post = Post(post_data)
        post.save()
        for i in range(int(images_number)):
            image = request.files.get("image"+str(i))
            if image and allowed_file(image.filename):
                image_data = imgur_handler.send_image(image)
                image_url = image_data["data"]["link"]
                image_delete_hash =  image_data["data"]["deletehash"]
                imageObj = PhotoImage({"post_id": post.id, "imageUrl": image_url, "del_hash": image_delete_hash})
                imageObj.save()
        return make_response(jsonify({'post': post_schema.dump(post), 'message': 'New post successfully successfully added.'})), 201
        
    @app.route('/api/v1/posts/country', methods=['GET'])
    @jwt_required
    def user_view_country_posts():
        current_user = get_jwt_identity()
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        country_posts = posts_schema.dump(Post.query.filter_by(country=current_user['country']))[::-1]
        for post in country_posts:
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = likes_schema.dump(Like.query.filter_by(post_id=post['id']))
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post['id']))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user['id']).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user['id']).first())
            post['poster'] = user
            post['likes'] = len(likes)
            post['comments'] = len(comments)
            post['images'] = images
            if liked:
                post['liked'] = True
            else: post['liked'] = False            
            if bookmarked:
                post['bookmarked'] = True
            else: post['bookmarked'] = False
        return make_response(jsonify({"posts":country_posts[start:end]}))

    #--------------------------------------------------------------------------------

    #--------------------------------------------------------------------------------

    @app.route('/api/v1/posts/country/<post_id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required
    def user_post_edit(post_id):
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

            
    @app.route('/api/v1/posts/bookmarked', methods=['GET'])
    @jwt_required
    def user_view_bookmarked_posts():
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        current_user = get_jwt_identity()
        bookmarks = bookmarks_schema.dump(Bookmark.query.filter_by(user_id=current_user['id']))[::-1]
        posts = []
        for bookmark in bookmarks:
            post = post_schema.dump(Post.query.get(bookmark['post_id']))
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = len(likes_schema.dump(Like.query.filter_by(post_id=post['id'])))
            comments = len(comments_schema.dump(Comment.query.filter_by(post_id=post['id'])))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user['id']).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user['id']).first())
            post['poster'] = user
            post['likes'] = likes
            post['comments'] = comments
            post['images'] = images
            if liked:
                post['liked'] = True
            else: post['liked'] = False            
            if bookmarked:
                post['bookmarked'] = True
            else: post['bookmarked'] = False
            posts.append(post)
        return make_response(jsonify({"bookmarked_posts":posts[start:end]}))

    
    @app.route('/api/v1/posts/user', methods=['GET'])
    @jwt_required
    def user_view_own_posts():
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        current_user = get_jwt_identity()
        user_posts = posts_schema.dump(Post.query.filter_by(posted_by=current_user['id']))[::-1]
        for post in user_posts:
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = len(likes_schema.dump(Like.query.filter_by(post_id=post['id'])))
            comments = len(comments_schema.dump(Comment.query.filter_by(post_id=post['id'])))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user['id']).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user['id']).first())
            post['poster'] = user
            post['likes'] = likes
            post['comments'] = comments
            post['images'] = images
            if liked:
                post['liked'] = True
            else: post['liked'] = False            
            if bookmarked:
                post['bookmarked'] = True
            else: post['bookmarked'] = False
        return make_response(jsonify({"posts":user_posts[start:end]}))


    # Comment endpoints ############################################################################################################

    @app.route('/api/v1/comments/post/<post_id>', methods=['GET','POST'])
    @jwt_required
    def user_add_new_comment(post_id):
        current_user = get_jwt_identity()
        if request.method == 'POST':
            message = request.data.get('message', '')
            user = User.query.get(current_user['id'])
            comment_obj = {"post_id": post_id, "message": message, "by": current_user['id']}
            comment = Comment(comment_obj)
            comment.save()
            return make_response(jsonify({"message": "comment successfully saved."}))
        if request.method == 'GET':
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post_id))[::-1]
            for comment in comments:
                user = user_schema.dump(User.query.get(comment['by']))
                comment['user'] = user
            return make_response(jsonify({"comments": comments}))

    @app.route('/api/v1/comments/<comment_id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required
    def user_crud_on_comment(comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            if request.method == 'GET':
                return make_response(jsonify({"comment": comment_schema.dumps(comment)}))
            if request.method == 'DELETE':
                comment.delete()
                return make_response(jsonify({"message": "Comment deleted successfully."}))
            if request.method == 'PUT':
                message = request.form.get('message', '')
                comment.add_added(message)
                comment.save()
                return make_response(jsonify({"message": "comment successfully updated."}))
        else:
            return make_response(jsonify({"comment not found."}))



    # Like endpoints ############################################################################################################

    @app.route('/api/v1/likes/post/<post_id>', methods=['POST'])
    @jwt_required
    def user_like_post(post_id):
        current_user = get_jwt_identity()
        like = Like.query.filter_by(post_id=post_id).filter_by(liked_by=current_user['id']).first()
        if not like:
            like_obj = {"post_id": post_id, "liked_by": current_user['id']}
            like = Like(like_obj)
            like.save()
            return make_response(jsonify({"message": "Like successfully saved."}))
        else:
            like.delete()
            return make_response(jsonify({"message": "Like successfully removed."}))

    
    # Bookmarks endpoints ############################################################################################################

    @app.route('/api/v1/bookmarks', methods=['GET'])
    @jwt_required
    def user_bookmarks():
        current_user = get_jwt_identity()
        bookmarks = Bookmark.query.filter_by(user_id = current_user['id'])
        return make_response(jsonify({"bookmarks": bookmarks_schema.dump(bookmarks)}))

    @app.route('/api/v1/bookmarks/posts/<post_id>', methods=['POST'])
    @jwt_required
    def user_bookmarked(post_id):
        current_user = get_jwt_identity()
        bookmark = Bookmark.query.filter_by(post_id=post_id).filter_by(user_id=current_user['id']).first()
        if bookmark:
            bookmark.delete()
            return make_response(jsonify({"message": "Bookmark successfully deleted."}))
        else:
            bookmark = Bookmark({'post_id': post_id, 'user_id': current_user['id']})
            bookmark.save()
            return make_response(jsonify({"message": "Book successfully saved!"})), 201

    # Search ######################################################################

    @app.route('/api/v1/search', methods=['POST'])
    @jwt_required
    def user_and_post_search():
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        search = request.data.get('search', '')
        current_user = get_jwt_identity()
        users = users_schema.dump(User.query.filter_by(country=current_user['country']).filter(User.name.ilike("%"+search+"%")).all())
        posts = posts_schema.dump(Post.query.filter_by(country=current_user['country']).filter(Post.message.ilike("%"+search+"%")).all())
        posts2 = posts_schema.dump(Post.query.filter_by(country=current_user['country']).filter(Post.tags.ilike("%"+search+"%")).all())

        posts = posts2 + posts

        for post in posts:
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = len(likes_schema.dump(Like.query.filter_by(post_id=post['id'])))
            comments = len(comments_schema.dump(Comment.query.filter_by(post_id=post['id'])))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user['id']).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user['id']).first())
            post['poster'] = user
            post['likes'] = likes
            post['comments'] = comments
            post['images'] = images
            if liked:
                post['liked'] = True
            else: post['liked'] = False            
            if bookmarked:
                post['bookmarked'] = True
            else: post['bookmarked'] = False
        return make_response(jsonify({"people_number": len(users), "people": users, "posts_number": len(posts), "posts": posts[start:end]}))
        

    # Feedback endpoints ############################################################################################################

    @app.route('/api/v1/feedback', methods=['GET','POST'])
    @jwt_required
    def user_new_feedback():
        if request.method == 'POST':
            message = request.data.get('message', '')
            rating = request.data.get('rating','')
            by = get_jwt_identity()['id']
            at = request.data.get('at','')
            feedback = Feedback({"message": message, "rating": rating, "by": by, "at": at})
            feedback.save()
            return make_response(jsonify({"message": "Delighted :)  Thanks for  the feedback!"})), 201
        if request.method == 'GET':
            all_feedback = feedbacks_schema.dump(Feedback.query.all())
            return make_response(jsonify({"feedback": all_feedback}))


    return app
