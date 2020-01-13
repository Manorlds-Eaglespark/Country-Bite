from shared import ma
from app.views import db

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    code = db.Column(db.Integer)
    time_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, code):
        self.name = name
        self.code = code
      
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CountrySchema(ma.Schema):
    class Meta:
        fields = ("name", "code", "time_added")

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
