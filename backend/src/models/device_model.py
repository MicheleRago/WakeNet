from sqlalchemy.orm import relationship
from src import db
from dataclasses import dataclass

@dataclass
class Device(db.Model):
    id: int
    name: str
    mac: str
    user_id: int

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    mac = db.Column(db.String(12))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Definiamo la relazione inversa con User
    user = relationship('User', back_populates='devices')