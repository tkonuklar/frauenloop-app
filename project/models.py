from datetime import datetime
from project import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account = db.relationship('Account', backref='owner',lazy=True)

    def __repr__(self):
        return f"User(name='{self.name}', pin='{self.name}', created_at='{self.created_at}')"


class Account(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Account(balance='{self.balance}', owner='{self.owner_id}', created_at='{self.created_at}')"
