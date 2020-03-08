from datetime import datetime
from shared import db, ma
from app.models.users import User

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.Integer, db.ForeignKey(User.id))
    rating = db.Column(db.Float)
    message = db.Column(db.String(255))
    at = db.Column(db.String(50))
    user = db.relationship('User', backref='feedback')

    def __init__(self, comment_object):
        """Initialize a feedback object"""
        self.rating = comment_object["rating"]
        self.message = comment_object["message"]
        self.by = comment_object["by"]
        self.at = comment_object["at"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class FeedbackSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "rating", "by", "message", "at")

feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)
