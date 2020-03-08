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
from app.helpers.validations import all_countries
from app.helpers.check_loggedin import login_required
from app.models.users import User, user_schema, users_schema
from app.models.posts import Post, post_schema, posts_schema
from app.models.reports import Report, report_schema, reports_schema
from app.models.comments import Comment, comment_schema, comments_schema
from app.models.likes import Like, like_schema, likes_schema
from app.models.bookmarks import Bookmark, bookmark_schema, bookmarks_schema
from app.models.countries import Country, country_schema, countries_schema
from app.models.images import PhotoImage, photoimage_schema, photoimages_schema
from app.models.shop.shops import Shop, shop_schema, shops_schema
from app.models.shop.ads import Ad, ad_schema, ads_schema
from app.models.shop.categories import Category, category_schema, categories_schema
from app.models.shop.products import Product, product_schema, products_schema
from app.models.shop.product_images import ProductImage, productimage_schema, productimages_schema
from app.helpers.validations import allowed_file

POSTS_PER_PAGE = 10

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMGUR_ID"] = os.getenv('IMGSER')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    ma = Marshmallow(app)
    imgur_handler = Imgur(app)
    CORS(app)

    with app.app_context():
        countries = countries_schema.dump(Country.query.all())
        if not countries:
            for country in all_countries:
                add_country = Country(country)
                add_country.save()

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
                country = Country.query.get(user.country)
                access_token = user.generate_token()
                return make_response(jsonify({"message":"You successfully logged-in.", "token": access_token.decode(), "country_name": country.name, "country_id": country.id, "country_flag": country.flag, "shopOwner": user.shopOwner}))
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
        about = "I love Countalk very much."
        country_detail = country_schema.dump(Country.query.filter_by(name=country).first())
        user_data = {"name": name, "country": country_detail['id'], "email": email, "about": about, "password": password, "phonenumber": phonenumber}
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


    # User endpoints ############################################################################################################

    @app.route('/api/v1/user', methods=['GET'])
    @login_required
    def get_user(current_user, country):
        user = user_schema.dump(User.query.get(current_user))
        country = country_schema.dump(Country.query.get(user['country']))
        user['country'] = country
        return make_response(jsonify({"user": user}))

    @app.route('/api/v1/user/edit', methods=['PUT'])
    @login_required
    def edit_user_detail(current_user, country):
        name = request.form.get('name','')
        about = request.form.get('about', '')
        email = request.form.get('email', '')
        profile_image = request.files.get('profile_image','')

        user = User.query.get(current_user)
        if user.profile_img and profile_image:
            imgur_handler.delete_image(delete_hash=user.img_del_hash)
        if profile_image:
            image_data = imgur_handler.send_image(profile_image)
            image_url = image_data["data"]["link"]
            image_delete_hash =  image_data["data"]["deletehash"]
            user.profile_img = image_url
            user.img_del_hash = image_delete_hash
        user.add_added({"name": name, "about": about, "email": email})
        user.save()
        return make_response(jsonify({"message":"User details successfully updated."})), 202
                

    #     country = country_schema.dump(Country.query.get(user['country']))
    #     user['country'] = country
    #     return make_response(jsonify({"user": user}))

    # Post endpoints ############################################################################################################

    @app.route('/api/v1/posts', methods=['POST'])
    @login_required
    def user_add_new_post(current_user, country):
        message = request.form.get('message', '')
        images_number = request.form.get('images_number')
        
        post_data = {"country": country, "message": message, "posted_by": current_user}
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
        return make_response(jsonify({'post': post_schema.dump(post), 'message': 'new post successfully successfully saved.'})), 201
        
    @app.route('/api/v1/posts/country', methods=['GET'])
    @login_required
    def user_view_country_posts(current_user, country):
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        country_posts = posts_schema.dump(Post.query.filter_by(country=country))[::-1]
        for post in country_posts:
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = likes_schema.dump(Like.query.filter_by(post_id=post['id']))
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post['id']))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user).first())
            post['poster_name'] = user['name']
            post['poster_about'] = user['about']
            post['poster_image'] = user['profile_img']
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

    # @app.route('/delete', methods=['GET'])
    # def delete_all_images_up():
    #     images = PhotoImage.query.all()
    #     for image in images:
    #         imgur_handler.delete_image(delete_hash=image.del_hash)
    #         image.delete()
    #     return {"msg": "Done"}

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

            
    @app.route('/api/v1/posts/bookmarked', methods=['GET'])
    @login_required
    def user_view_bookmarked_posts(current_user, country):
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        bookmarks = bookmarks_schema.dump(Bookmark.query.filter_by(user_id=current_user))[::-1]
        posts = []
        for bookmark in bookmarks:
            post = post_schema.dump(Post.query.get(bookmark['post_id']))
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = likes_schema.dump(Like.query.filter_by(post_id=post['id']))
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post['id']))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user).first())
            post['poster_name'] = user['name']
            post['likes'] = len(likes)
            post['comments'] = len(comments)
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
    @login_required
    def user_view_own_posts(current_user, country):
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        user_posts = posts_schema.dump(Post.query.filter_by(posted_by=current_user))[::-1]
        for post in user_posts:
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = likes_schema.dump(Like.query.filter_by(post_id=post['id']))
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post['id']))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user).first())
            post['poster_name'] = user['name']
            post['likes'] = len(likes)
            post['comments'] = len(comments)
            post['images'] = images
            if liked:
                post['liked'] = True
            else: post['liked'] = False            
            if bookmarked:
                post['bookmarked'] = True
            else: post['bookmarked'] = False
        return make_response(jsonify({"posts":user_posts[start:end]}))


    # Report endpoints ############################################################################################################

    @app.route('/api/v1/reports', methods=['GET','POST'])
    @login_required
    def user_add_new_report(current_user, country):
        if request.method == 'POST':
            post_id = request.data.get('post', 0)
            reason = request.data.get('reason', '')
            report = Report.query.filter_by(post_id=post_id)
            if not report:
                report_data = {"status":"new", "reason": reason, "by":current_user, "post_id":post_id}
                report = Report(report_data)
                report.save()
                return make_response(jsonify({"message":"Thanks for reporting this."}))
            else:
                report.add_added(report_data)
                report.save()
                return make_response(jsonify({"message":"report successfully updated."}))
        if request.method == 'GET':
            reports = Report.query.all()
            return make_response(jsonify({"reports":reports}))



    # Comment endpoints ############################################################################################################

    @app.route('/api/v1/comments/post/<post_id>', methods=['GET','POST'])
    @login_required
    def user_add_new_comment(current_user, country, post_id):
        if request.method == 'POST':
            message = request.data.get('message', '')
            user = User.query.get(current_user)
            comment_obj = {"post_id": post_id, "message": message, "by": current_user}
            comment = Comment(comment_obj)
            comment.save()
            return make_response(jsonify({"message": "comment successfully saved."}))
        if request.method == 'GET':
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post_id))
            for comment in comments:
                user = User.query.get(comment['by'])
                comment['user_name'] = user.name
                comment['user_image'] = user.profile_img
                comment['user_about'] = user.about
            return make_response(jsonify({"comments": comments}))

    @app.route('/api/v1/comments/<comment_id>', methods=['GET', 'PUT', 'DELETE'])
    @login_required
    def user_crud_on_comment(current_user, country, comment_id):
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
    @login_required
    def user_like_post(current_user, country, post_id):
        like = Like.query.filter_by(post_id=post_id).filter_by(liked_by=current_user).first()
        if not like:
            like_obj = {"post_id": post_id, "liked_by": current_user}
            like = Like(like_obj)
            like.save()
            return make_response(jsonify({"message": "Like successfully saved."}))
        else:
            like.delete()
            return make_response(jsonify({"message": "Like successfully removed."}))

    
    # Bookmarks endpoints ############################################################################################################

    @app.route('/api/v1/bookmarks', methods=['GET'])
    @login_required
    def user_bookmarks(current_user, country):
        bookmarks = Bookmark.query.filter_by(user_id = current_user)
        return make_response(jsonify({"bookmarks": bookmarks_schema.dump(bookmarks)}))

    @app.route('/api/v1/bookmarks/posts/<post_id>', methods=['POST'])
    @login_required
    def user_bookmarked(current_user, country, post_id):
        bookmark = Bookmark.query.filter_by(post_id=post_id).filter_by(user_id=current_user).first()
        if bookmark:
            bookmark.delete()
            return make_response(jsonify({"message": "Bookmark successfully deleted."}))
        else:
            bookmark = Bookmark({'post_id': post_id, 'user_id': current_user})
            bookmark.save()
            return make_response(jsonify({"message": "Book successfully saved!"})), 201

    # Search ######################################################################

    @app.route('/api/v1/search', methods=['POST'])
    @login_required
    def user_and_post_search(current_user, country):
        page = int(request.args.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        search = request.data.get('search', '')
        users = users_schema.dump(User.query.filter_by(country=country).filter(User.name.ilike("%"+search+"%")).all())
        posts = posts_schema.dump(Post.query.filter_by(country=country).filter(Post.message.ilike("%"+search+"%")).all())[::-1]
        for post in posts:
            user = user_schema.dump(User.query.get(post['posted_by']))
            likes = likes_schema.dump(Like.query.filter_by(post_id=post['id']))
            comments = comments_schema.dump(Comment.query.filter_by(post_id=post['id']))
            images = photoimages_schema.dump(PhotoImage.query.filter_by(post_id=post['id']))
            liked = like_schema.dump(Like.query.filter_by(post_id=post['id']).filter_by(liked_by=current_user).first())
            bookmarked = bookmark_schema.dump(Bookmark.query.filter_by(post_id=post['id']).filter_by(user_id=current_user).first())
            post['poster_name'] = user['name']
            post['poster_about'] = user['about']
            post['poster_image'] = user['profile_img']
            post['likes'] = len(likes)
            post['comments'] = len(comments)
            post['images'] = images
            if liked:
                post['liked'] = True
            else: post['liked'] = False            
            if bookmarked:
                post['bookmarked'] = True
            else: post['bookmarked'] = False
        return make_response(jsonify({"people_number": len(users), "people": users, "posts_number": len(posts), "posts": posts[start:end]}))
        
        
    # Shop endpoints ############################################################################################################

    @app.route('/api/v1/shops', methods=['GET','POST'])
    @login_required
    def user_new_shop(current_user, country):
        if request.method == 'GET':
            shop = shop_schema.dump(Shop.query.filter_by(owner=current_user).first())
            if shop:
                shop['categories'] = categories_schema.dump(Category.query.filter_by(shop_id=shop['id']))
                return make_response(jsonify({"shop": shop}))
            else:
                return make_response(jsonify({"error": "Create Shop first."})), 400

        if request.method == 'POST':
            owns_shop = Shop.query.filter_by(owner=current_user).first()
            if owns_shop:
                return make_response(jsonify({"error": "You can only have one shop here."})), 400
            shop_data = request.data.get('shop')
            name = shop_data['name']
            owner = current_user
            description = shop_data['description']
            telephone = shop_data['telephone']
            delivery = shop_data['delivery']
            address = shop_data['address']
            shop = Shop({"name": name, "owner": owner, "description": description, "telephone": telephone, "delivery": delivery, "address": address})
            user = User.query.get(current_user)
            user.shopOwner = 1
            user.save()
            shop.save()
            return make_response(jsonify({'shop': shop_schema.dump(shop), 'message': 'New shop successfully saved.'})), 201


    # Category crud endpoints ############################################################################################################
    
    @app.route('/api/v1/shops/categories/<category_id>', methods=['POST','PUT','DELETE'])
    @login_required
    def user_edit_category(current_user, country, category_id):
        category = Category.query.get(category_id)
        if category:
            if request.method == 'DELETE':
                category.delete()
                return make_response(jsonify({"message": "Category successfully deleted."}))
            if request.method == 'PUT':
                category_detail = request.data.get('category')
                category.add_added(category_detail)
                category.save()
                return make_response(jsonify({"message": "Category details successfully updated."}))
        else: 
            return make_response(jsonify({"error": "Category does not exist."})), 404
            


     # Products endpoints ############################################################################################################

    @app.route('/api/v1/shops/categories/<category_id>/products', methods=['GET','POST'])
    @login_required
    def user_new_product(current_user, country, category_id):
        if request.method == 'GET':
            products = products_schema.dump(Product.query.filter_by(category_id=category_id).all())
            for product in products:
                product['images'] = productimages_schema.dump(ProductImage.query.filter_by(product_id=product['id']))
            return make_response(jsonify({"products": products}))
        
        if request.method == 'POST':
            product_data = request.data.get('product')
            name = product_data['name']
            description = product_data['description']
            use_status = product_data['use_status']
            price = product_data['price']

            product = Product({"name": name, "description": description, "use_status": use_status, "category_id": category_id, "price": price})
            product.save()
            return make_response(jsonify({'product': product_schema.dump(product), 'message': 'New product successfully saved.'})), 201

        
    @app.route('/api/v1/products/<product_id>/images', methods=['GET','POST'])
    @login_required
    def product_images(current_user, country, product_id):
        image = request.files.get("image")
        if image and allowed_file(image.filename):
            image_data = imgur_handler.send_image(image)
            image_url = image_data["data"]["link"]
            image_delete_hash =  image_data["data"]["deletehash"]
            imageObj = ProductImage({"product_id": product_id, "imageUrl": image_url, "del_hash": image_delete_hash})
            imageObj.save()
            return make_response(jsonify({"message": "image successfully added.", "image": productimage_schema.dump(imageObj)}))
        else:
            return make_response(jsonify({"error": "Add file with an jpg/png format"}))

 
    # Delete product image endpoint ############################################################################################################

    @app.route('/api/v1/products/images/<image_id>', methods=['DELETE'])
    @login_required
    def delete_images(current_user, country, image_id):
        image = ProductImage.query.get(image_id)
        if image:
            imgur_handler.delete_image(delete_hash=image.del_hash)
            image.delete()
            return make_response(jsonify({"message": "deleted successfully."})), 202
        else:
            return make_response(jsonify({"error": "Image not found."})), 404
 

    @app.route('/api/v1/shops/categories/products/<product_id>', methods=['PUT','DELETE'])
    @login_required
    def user_edit_product(current_user, country, product_id):
        product = Product.query.get(product_id)
        if product:
            if request.method == 'DELETE':
                product.delete()
                return make_response(jsonify({"message": "Product successfully deleted."}))
            if request.method == 'PUT':
                product_detail = request.data.get('product')
                product.add_added(product_detail)
                product.save()
                return make_response(jsonify({"message": "Product details successfully updated."}))
        else: 
            return make_response(jsonify({"error": "Product does not exist."})), 404

    
    # Ad endpoints ############################################################################################################

    @app.route('/api/v1/ads', methods=['GET','POST'])
    @login_required
    def user_new_ad(current_user, country):
        if request.method == 'GET':
            ads = ads_schema.dump(Ad.query.filter_by(country=country))
            for ad in ads:
                product  = product_schema.dump(Product.query.get(ad['product_id']))
                product['images'] = productimages_schema.dump(ProductImage.query.filter_by(product_id=ad['product_id']))
                ad['product']  = product
                ad['shop']  = shop_schema.dump(Shop.query.get(ad['shop_id']))
            return make_response(jsonify({"ads": ads}))

        if request.method == 'POST':
            ad_detail = request.data.get('ad', '')
            ad_detail['status'] = 1
            ad_detail['country'] = int(country)
            new_ad = Ad(ad_detail)
            new_ad.save()
            return make_response(jsonify({"message": "Ad successfully created."})), 201
       
            


    return app
