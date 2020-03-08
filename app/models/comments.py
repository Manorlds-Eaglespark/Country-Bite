from datetime import datetime
from shared import db, ma
from app.models.users import User
from app.models.posts import Post

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    message = db.Column(db.String(255))
    by = db.Column(db.Integer, db.ForeignKey(User.id))
    at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='comment')
    post = db.relationship('Post', backref='comment')

    def __init__(self, comment_object):
        """Initialize a Comment object"""
        self.post_id = comment_object["post_id"]
        self.message = comment_object["message"]
        self.by = comment_object["by"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_added(self, msg):
        if msg != '':
            self.message = msg


class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "post_id", "message", "by", "at")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
