from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    products = db.relationship('Product', backref='owner', lazy=True)
    offers = db.relationship('Offer', backref='offerer', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    offers = db.relationship(
        'Offer',
        backref='product',
        lazy=True,
        foreign_keys='Offer.product_id'
    )

    def __repr__(self):
        return f"<Product {self.title}>"

    
    
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    offered_product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    offerer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offered_product = db.relationship('Product', foreign_keys=[offered_product_id], backref='offered_in_offers')

