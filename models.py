from flask_login import UserMixin
from extensions import db  # ✅ Corrigé ici
from datetime import datetime
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    poids = db.Column(db.Float, nullable=True)
    quantite = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='meals')