from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,DateField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,Length,Email,optional,EqualTo

class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(),Length(4,15)]
    )
        
    email = StringField(
        "Email",
        validators=[DataRequired(),Email()]
    )

    gender = SelectField(
        "Gender",
        choices=["Male", "Female","Custom"],
        validators=[optional()]
    )

    dob = DateField(
        "Date Of Birth",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(),Length(5,15)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(),Length(5,15),EqualTo("password")]
    )

    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(),Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(),Length(5,15)]
    )

    remember = BooleanField(
        "Remember Me"
    )

    submit = SubmitField("Login")

class OrderForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(),Email()]
    )
    contact = StringField(
        'contact',
        validators=[DataRequired(),Length(10)]
    )
    street = StringField(
        'street',
        validators=[DataRequired(), Length(5,50)]
    )
    city = StringField(
        'City',
        validators=[DataRequired(), Length(3,15)]
    )
    state = StringField(
        'State',
        validators=[DataRequired(), Length(3,20)]
    )
    zip_code = StringField(
        'Zip Code',
        validators=[DataRequired(), Length(6)]
    )
    submit = SubmitField("Place Order")