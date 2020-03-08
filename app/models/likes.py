import datetime
from shared import db, ma
from app.models.users import User
from app.models.posts import Post

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    liked_by = db.Column(db.Integer, db.ForeignKey(User.id))
    liked_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='like')
    post = db.relationship('Post', backref='like')

    def __init__(self, like_object):
        """Initialize a Post object"""
        self.post_id = like_object["post_id"]
        self.liked_by = like_object["liked_by"]
        self.liked_at = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class LikeSchema(ma.Schema):
    class Meta:
        fields = ("id", "post_id", "liked_by", "liked_at")

like_schema = LikeSchema()
likes_schema = LikeSchema(many=True)
