from flask import session
from db import db
from sqlalchemy.dialects.mysql import JSON

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    password = db.Column(db.String(60))
    cart = db.Column(db.String(255), default="")
    orders = db.Column(db.String(255), default="")

    def user_Details(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "gender": self.gender,
            "dob": self.dob.strftime('%Y-%m-%d') if self.dob else None,
            "cart": self.cart,
            "orders": self.orders
        }

def addUser(username,email,gender,dob,password):
    user = User.query.filter_by(email=email).first()
    print(user)
    if user:
        return False
    else:
        new_user = User(username=username, email=email, gender=gender, dob=dob, password=password)
        db.session.add(new_user)
        db.session.commit()
        return True

def add_To_cart(product_id):
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return False
    cart_list = user.cart.split(",") if user.cart else []
    if str(product_id) not in cart_list:
        cart_list.append(str(product_id))
        user.cart = ",".join(cart_list)
        db.session.commit()
        return True
    else:
        return False

def validateUser(email,password):
    print("Validate")
    email = User.query.filter_by(email=email).first()
    print("ValidateUser")
    if not email:
        return False
    if email.password == password:
        return True
    else:
        return False
    
def addSession(email):
    session['email'] = email

def isLoggedIn():
    if 'email' in session:
        try:
            user = User.query.filter_by(email=session['email']).first()
            if not user:
                return None
            Curruser = user.user_Details()
            Curruser['email'] = session['email']
            return Curruser
        except Exception as e:
            return None
    else:
        return None
    
def addOrderId(id):
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return False
    orders_list = user.orders.split(",") if user.orders else []
    if str(id) not in orders_list:
        orders_list.append(str(id))
        user.orders = ",".join(orders_list)
        db.session.commit()
        return True
    else:
        return False
    
def removeFromCart(product_id):
    user = User.query.filter_by(email=session['email']).first()
    if not user:
        return False
    cart_list = user.cart.split(",") if user.cart else []
    if str(product_id) in cart_list:
        cart_list.remove(str(product_id))
        user.cart = ",".join(cart_list)
        db.session.commit()
        return True
    else:
        return False
def getAllUsers():
    users = User.query.all()
    allUsers = []
    for user in users:
        temp = user.user_Details()
        allUsers.append(temp)
    return allUsers
    
def logoutUser():
    session.pop('email', None)
    return True
