from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired
from netmiko.ssh_dispatcher import CLASS_MAPPER

class AddUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add User')

class AddDevice(FlaskForm):
    friendly_name = StringField('Friendly Name', validators=[DataRequired()])
    ip = StringField('IP Address', validators=[DataRequired()])
    netmiko_driver = SelectField('Netmiko Driver', choices=[driver for driver in CLASS_MAPPER.keys()], validators=[DataRequired()])
    authentication_user = SelectField('User', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Device')