from models.models import User
from app import db

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

def register_user(name, email, password):
    if User.query.filter_by(email=email).first():
        return None
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    return user
