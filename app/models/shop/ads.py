import datetime
from shared import db, ma
from app.models.users import User
from app.models.shop.products import Product
from app.models.shop.shops import Shop

class Ad(db.Model):
    __tablename__ = 'ads'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    status = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    shop_id = db.Column(db.Integer, db.ForeignKey(Shop.id))
    discounted_price = db.Column(db.String(50))
    duration = db.Column(db.String(40))
    posted_at = db.Column(db.String(40))
    country = db.Column(db.Integer)
    product = db.relationship('Product', backref='ad')
    shop = db.relationship('Shop', backref='ad')

    def __init__(self, ad_object):
        """Initialize a Ad object"""
        self.description = ad_object["description"]
        self.status = ad_object["status"]
        self.product_id = ad_object["product_id"]
        self.shop_id = ad_object["shop_id"]
        self.discounted_price = ad_object["discounted_price"]
        self.duration = ad_object["duration"]
        self.country = ad_object["country"]
        self.posted_at = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class AdSchema(ma.Schema):
    class Meta:
        fields = ("id", "message", "status", "description", "product_id", "shop_id", "discounted_price", "duration", "country", "posted_at")

ad_schema = AdSchema()
ads_schema = AdSchema(many=True)
