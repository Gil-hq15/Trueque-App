import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from models.models import Product, Offer
from forms.forms import ProductForm, BarterOfferForm

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
            os.makedirs(upload_path, exist_ok=True)
            form.image.data.save(os.path.join(upload_path, filename))
        
        product = Product(
            title=form.title.data,
            description=form.description.data,
            image_filename=filename,
            owner=current_user
        )
        db.session.add(product)
        db.session.commit()
        flash('Producto publicado con éxito.', 'success')
        return redirect(url_for('main.home'))
    return render_template('products/new.html', form=form)

@products_bp.route('/products/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    form = BarterOfferForm()

    if current_user.is_authenticated:
        user_products = Product.query.filter_by(owner_id=current_user.id).all()
        form.offered_product_id.choices = [(p.id, p.title) for p in user_products if p.id != product.id]

    if form.validate_on_submit():
        offer = Offer(
            product_id=product.id,
            offered_product_id=form.offered_product_id.data,
            offerer_id=current_user.id
        )
        db.session.add(offer)
        db.session.commit()
        flash("¡Oferta de trueque enviada!", "success")
        return redirect(url_for('main.home'))

    offers = Offer.query.filter_by(product_id=product.id).all()

    return render_template('products/detail.html', product=product, form=form, offers=offers)
