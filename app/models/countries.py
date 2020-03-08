import datetime
from shared import db, ma

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    flag = db.Column(db.String(255))
    created_at = db.Column(db.String(100))

    def __init__(self, country_object):
        """Initialize a Country object"""
        self.name = country_object["name"]
        self.flag = country_object["flag"]
        self.created_at = datetime.datetime.now()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CountrySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "flag", "created_at")

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)
