from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired

from models.models import User
from app import db

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('El nombre de usuario ya existe. Escoge otro.')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ProductForm(FlaskForm):
    title = StringField('Título del producto', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Descripción', validators=[Length(max=500)])
    image = FileField('Imagen del producto', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo imágenes!')])
    submit = SubmitField('Publicar')

class OfferForm(FlaskForm):
    message = TextAreaField('Mensaje para la oferta (opcional)', validators=[Length(max=300)])
    submit = SubmitField('Hacer oferta')


class BarterOfferForm(FlaskForm):
    offered_product_id = SelectField('¿Qué producto ofreces a cambio?', coerce=int, validators=[DataRequired()])
    submit = SubmitField('+ Ofrecer Trueque')