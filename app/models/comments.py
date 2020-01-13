from shared import ma
from app.views import db
from app.models.users import User
from app.models.posts import Post

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.Integer, db.ForeignKey(Post.id))
    message = db.Column(db.String(255))
    time_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    users = db.relationship('User', backref='comment')
    posts = db.relationship('Post', backref='comment')

    def __init__(self, name, code):
        self.name = name
        self.code = code
      
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "post", "message", "time_added")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
