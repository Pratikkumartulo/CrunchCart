from app import db
from sqlalchemy.dialects.mysql import JSON

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120))
    items = db.Column(JSON)
    timestamp = db.Column(db.DateTime)
    address = db.Column(db.String(200))
    contact = db.Column(db.Integer)
