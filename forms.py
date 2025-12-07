"""
Forms - Using Flask-WTF for validation
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, DateField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class PlayerForm(FlaskForm):
    """Player form"""
    name = StringField('Nombre del Jugador', validators=[DataRequired(), Length(max=100)])
    minecraft_username = StringField('Usuario de Minecraft', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Guardar')

class PaymentForm(FlaskForm):
    """Payment form"""
    player_id = SelectField('Jugador', coerce=int, validators=[DataRequired()])
    amount = DecimalField('Monto (S/)', validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Fecha', validators=[DataRequired()])
    description = TextAreaField('Descripción (Opcional)')
    submit = SubmitField('Guardar')

class ExpenseForm(FlaskForm):
    """Expense form"""
    amount = DecimalField('Monto (S/)', validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Fecha', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Guardar')
