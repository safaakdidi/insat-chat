from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,SubmitField
from wtforms.validators import InputRequired,Length,EqualTo,ValidationError
import sign
import utils
import hashlib
def invalidCredentials(form,field):
    login_entered=form.email.data
    pwd_entered=field.data

    user=sign.signIn(login_entered,pwd_entered)
    if user is None:
        raise ValidationError('userName or password not correct')
    # if utils.verifyCert(user[7]) == False:
    #     raise ValidationError('certificate not valid')







class RegistrationForm(FlaskForm):
    nom = StringField('name', validators=[InputRequired(message='first name required')])
    prenom = StringField('lastName', validators=[InputRequired(message='last name required')])
    num_card = StringField('cardNum', validators=[InputRequired(message='card num required')])
    pseudo = StringField('userName', validators=[InputRequired(message='username required')])
    email = EmailField('email', validators=[InputRequired(message='email required')])
    pwd = PasswordField('pwd', validators=[InputRequired(message='password required'),Length(min=4,message='password length must be greater than 3 ')])
    submit_button=SubmitField('Register')

class LoginForm(FlaskForm):
    email=EmailField('email',validators=[InputRequired(message='email required')])
    pwd=PasswordField('pwd',validators=[InputRequired(message='password required'),invalidCredentials])
    submit_button=SubmitField('Login')

