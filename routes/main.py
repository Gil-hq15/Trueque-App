from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('main/home.html', products=products)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')
