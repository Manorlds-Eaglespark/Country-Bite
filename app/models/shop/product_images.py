import datetime
from shared import db, ma
from app.models.shop.products import Product

class ProductImage(db.Model):
    __tablename__ = 'productimages'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
    imageUrl = db.Column(db.String(255))
    del_hash = db.Column(db.String(255))
    product = db.relationship('Product', backref='productimage')

    def __init__(self, productimage_object):
        """Initialize a Product object"""
        self.product_id = productimage_object["product_id"]
        self.imageUrl = productimage_object["imageUrl"]
        self.del_hash = productimage_object["del_hash"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ProductImageSchema(ma.Schema):
    class Meta:
        fields = ("imageUrl","id")

productimage_schema = ProductImageSchema()
productimages_schema = ProductImageSchema(many=True)
