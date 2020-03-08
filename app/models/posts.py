import datetime
from shared import db, ma
from app.models.users import User

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    country = db.Column(db.Integer)
    posted_by = db.Column(db.Integer, db.ForeignKey(User.id))
    posted_at = db.Column(db.String(25))
    user = db.relationship('User', backref='post')

    def __init__(self, post_object):
        """Initialize a Post object"""
        self.country = post_object["country"]
        self.message = post_object["message"]
        self.posted_by = post_object["posted_by"]
        self.posted_at = datetime.datetime.now()
    
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
