from datetime import datetime
from shared import db, ma
from app.models.users import User
from app.models.posts import Post

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))
    reason = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    by = db.Column(db.Integer, db.ForeignKey(User.id))
    at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='report')
    post = db.relationship('Post', backref='report')

    def __init__(self, report_object):
        """Initialize a Report object"""
        self.status = report_object["status"]
        self.by = report_object["by"]
        self.reason = report_object["reason"]
        self.post_id = report_object["post_id"]
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_added(self, status):
        if status != '':
            self.status = status
        if reason != '':
            self.reason = reason


class ReportSchema(ma.Schema):
    class Meta:
        fields = ("id", "status", "post_id", "reason", "by", "at")

report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)
