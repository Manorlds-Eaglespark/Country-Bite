import datetime
from shared import db, ma
from app.models.users import User

class Shop(db.Model):
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    telephone = db.Column(db.String(30))
    description = db.Column(db.String(255))
    delivery = db.Column(db.String(50))
    address = db.Column(db.String(50))
    image = db.Column(db.String(100))
    image_del_hash = db.Column(db.String(100))
    created_on = db.Column(db.String(40))
    user = db.relationship('User', backref='shop')

    def __init__(self, shop_object):
        """Initialize a Ad object"""
        self.name = shop_object["name"]
        self.owner = shop_object["owner"]
        self.description = shop_object["description"]
        self.telephone = shop_object["telephone"]
        self.delivery = shop_object["delivery"]
        self.address = shop_object["address"]
        self.created_on = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "owner", "telephone", "delivery", "description", "address", "image", "created_on")

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)
