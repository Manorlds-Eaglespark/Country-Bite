import datetime
from shared import db, ma
from app.models.users import User
from app.models.shop.categories import Category

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    use_status = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    price = db.Column(db.String(50))
    posted_at = db.Column(db.String(40))
    category = db.relationship('Category', backref='product')

    def __init__(self, product_object):
        """Initialize a Product object"""
        self.name = product_object["name"]
        self.description = product_object["description"]
        self.use_status = product_object["use_status"]
        self.category_id = product_object["category_id"]
        self.price = product_object["price"]
        self.posted_at = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def add_added(self, product_data):
        if product_data['name']:
            self.name = product_data['name']
        if product_data['description']:
            self.description = product_data['description']
        if product_data['use_status']:
            self.use_status = product_data['use_status']
        if product_data['price']:
            self.price = product_data['price']

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "use_status", "category_id", "price", "posted_at")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
