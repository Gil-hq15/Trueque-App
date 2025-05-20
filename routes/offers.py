from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models.models import Product, Offer
from forms.forms import OfferForm

offers_bp = Blueprint('offers', __name__, url_prefix='/offers')

@offers_bp.route('/make/<int:product_id>', methods=['GET', 'POST'])
@login_required
def make_offer(product_id):
    product = Product.query.get_or_404(product_id)
    if product.owner == current_user:
        flash('No puedes hacer una oferta a tu propio producto.', 'warning')
        return redirect(url_for('products.product_detail', product_id=product_id))
    form = OfferForm()
    if form.validate_on_submit():
        offer = Offer(
            message=form.message.data,
            product=product,
            offerer=current_user
        )
        db.session.add(offer)
        db.session.commit()
        flash('Oferta realizada con éxito.', 'success')
        return redirect(url_for('products.product_detail', product_id=product_id))
    return render_template('offers/make_offer.html', form=form, product=product)
