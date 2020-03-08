import datetime
from shared import db, ma
from app.models.users import User
from app.models.posts import Post

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created_at =db.Column(db.String(100))
    user = db.relationship('User', backref='bookmark')
    post = db.relationship('Post', backref='bookmark')

    def __init__(self, bookmark_object):
        """Initialize a Comment object"""
        self.post_id = bookmark_object["post_id"]
        self.user_id = bookmark_object["user_id"]
        self.created_at = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class BookmarkSchema(ma.Schema):
    class Meta:
        fields = ("id", "post_id", "user_id", "created_at")

bookmark_schema = BookmarkSchema()
bookmarks_schema = BookmarkSchema(many=True)