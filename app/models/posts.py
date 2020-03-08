from datetime import datetime
from shared import db, ma
from app.models.users import User

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    image_url = db.Column(db.String(100))
    country = db.Column(db.String(100))
    image_delete_hash = db.Column(db.String(100))
    posted_by = db.Column(db.Integer, db.ForeignKey(User.id))
    posted_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='cart')

    def __init__(self, post_object):
        """Initialize a Post object"""
        self.country = post_object["country"]
        self.message = post_object["message"]
        self.image_url = post_object["image_url"]
        self.image_delete_hash = post_object["image_delete_hash"]
        self.posted_by = post_object["posted_by"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_added(self, msg):
        if msg != '':
            self.message = msg


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "message", "image_url", "country", "posted_by", "posted_at")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
