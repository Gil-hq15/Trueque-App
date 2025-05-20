from models.models import Product, Offer
from app import db
from werkzeug.utils import secure_filename
import os
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_product(user_id, title, description, category, state, file):
    filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    product = Product(
        user_id=user_id,
        title=title,
        description=description,
        category=category,
        state=state,
        image_filename=filename
    )
    db.session.add(product)
    db.session.commit()
    return product

def get_all_products():
    return Product.query.order_by(Product.created_at.desc()).all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)
