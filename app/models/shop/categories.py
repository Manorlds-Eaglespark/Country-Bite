import datetime
from shared import db, ma
from app.models.users import User
from app.models.shop.shops import Shop

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    shop_id = db.Column(db.Integer, db.ForeignKey(Shop.id))
    created_on = db.Column(db.String(40))
    shop = db.relationship('Shop', backref='category')

    def __init__(self, category_object):
        """Initialize a Ad object"""
        self.name = category_object["name"]
        self.shop_id = category_object["shop_id"]
        self.created_on = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_added(self, category_data):
        if category_data['name']:
            self.name = category_data['name']
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "shop_id", "created_on")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
