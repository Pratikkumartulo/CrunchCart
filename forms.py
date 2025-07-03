from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,DateField,PasswordField,SubmitField,BooleanField,IntegerField, TextAreaField
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
    quantity = SelectField(
        'Quantity',
        choices=[(str(i), str(i)) for i in range(1, 6)],  # Options 1-5
        validators=[DataRequired()]
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

class CartOrderForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    contact = StringField(
        "Contact",
        validators=[DataRequired(), Length(min=10, max=10)]
    )
    street = StringField(
        "Street",
        validators=[DataRequired(), Length(min=5, max=50)]
    )
    city = StringField(
        "City",
        validators=[DataRequired(), Length(min=3, max=15)]
    )
    state = StringField(
        "State",
        validators=[DataRequired(), Length(min=3, max=20)]
    )
    zip_code = StringField(
        "Zip Code",
        validators=[DataRequired(), Length(min=6, max=6)]
    )
    submit = SubmitField("Place Order")

class OrderStatusForm(FlaskForm):
    status = SelectField(
        "Update Status",
        choices=[
            ("Pending", "Pending"),
            ("Processing", "Processing"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Update Status")

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(2, 50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(10, 1000)])
    submit = SubmitField('Send Message')

class ReviewForm(FlaskForm):
    rating = SelectField(
        "Rating",
        choices=["5","4","3","2","1"],
        validators=[DataRequired()]
    )
    content = TextAreaField("Review", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Submit Review")
