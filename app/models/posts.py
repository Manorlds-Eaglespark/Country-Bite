from shared import ma
from app.views import db
from app.models.countries import Country
from app.models.users import User

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    country = db.Column(db.Integer, db.ForeignKey(Country.id))
    message = db.Column(db.String(255))
    image = db.Column(db.String(255))
    time_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    users = db.relationship('User', backref='post')
    countries = db.relationship('Country', backref='post')

    def __init__(self, user, country, message, image):
        self.user = user
        self.country = country
        self.message = message
        self.image = image
       
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

 
class PostSchema(ma.Schema):
    class Meta:
        fields = ("user", "country", "message", "image", "time_added")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
