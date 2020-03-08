import datetime
from shared import db, ma
from app.models.posts import Post

class PhotoImage(db.Model):
    __tablename__ = 'photoimages'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    imageUrl = db.Column(db.String(255))
    del_hash = db.Column(db.String(255))
    post = db.relationship('Post', backref='photoimage')

    def __init__(self, photoimage_object):
        """Initialize a Post object"""
        self.post_id = photoimage_object["post_id"]
        self.imageUrl = photoimage_object["imageUrl"]
        self.del_hash = photoimage_object["del_hash"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class PhotoImageSchema(ma.Schema):
    class Meta:
        fields = ("imageUrl", "id",)

photoimage_schema = PhotoImageSchema()
photoimages_schema = PhotoImageSchema(many=True)
