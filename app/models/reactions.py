from shared import ma
from app.views import db
from app.models.users import User
from app.models.posts import Post

class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    post = db.Column(db.Integer, db.ForeignKey(Post.id))
    scale = db.Column(db.String(255))
    time_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    users = db.relationship('User', backref='reaction')
    posts = db.relationship('Post', backref='reaction')

    def __init__(self, name, code):
        self.name = name
        self.code = code
      
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ReactionSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "post", "scale", "time_added")

reaction_schema = ReactionSchema()
reactions_schema = ReactionSchema(many=True)
