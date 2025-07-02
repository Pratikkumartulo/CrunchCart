from db import db
from flask import Flask, flash, render_template, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from forms import SignupForm, LoginForm, OrderForm
from chips import chipsData,findMaxThreeDiscount
from users import addUser,validateUser,addSession,isLoggedIn,logoutUser,add_To_cart
from config import DATABASE_URI, SECRET_KEY,SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route("/")
@app.route("/home")
def home():
    email = isLoggedIn()
    discounted = findMaxThreeDiscount(chipsData)
    return render_template("home.html",title="Home",chips = discounted,user=email)

@app.route("/about")
def about():
    email = isLoggedIn()
    return render_template("about.html",title="About",user=email)

@app.route("/contact") 
def contact():
    email = isLoggedIn()
    return render_template("contact.html",title="contact",user=email)


@app.route("/favourites") 
def favourites():
    email = isLoggedIn()
    return render_template("favourites.html",title="favourites",chipsData = chipsData,user=email)


@app.route("/products")
def products():
    email = isLoggedIn()
    return render_template("products.html",title="products",chips = chipsData,user=email)

@app.route('/user')
def userProfile():
    curUser = isLoggedIn()
    if curUser:
        return render_template('user.html', title='User',user = curUser)
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if validateUser(form.email.data,form.password.data):
            flash('Login successfull!','success')
            addSession(form.email.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password','error')

    return render_template('login.html', title="Login", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if addUser(form.username.data,form.email.data,form.gender.data,form.dob.data,form.password.data):
            addSession(form.email.data)
            flash(f'Signup successful! Welcome {form.username.data}!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Email already exists !!','error')

    return render_template('signup.html', title="Signup", form=form)

@app.route("/product/<id>")
def ProductDetail(id):
    email = isLoggedIn()
    if email:
        chip = chipsData.get(int(id))
        if not chip:
            return redirect(url_for('products'))
        return render_template('product_detail.html',title=f"CrunchCart - {chip['name']}",chipDet = chip,user=email,id=id)
    else:
        flash("You need to login for this action","info")
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    logoutUser()
    return redirect(url_for('home'))


@app.route('/order',methods=['GET','POST'])
def order():
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action","info")
        return redirect(url_for('login')) 
    form = OrderForm()
    return render_template("order.html",title="order",form=form,user=email)

@app.route('/cart')
def cart():
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action","info")
        return redirect(url_for('login')) 
    ids = email['cart'].split(',')
    # also add id = id in products
    products = [{"product": chipsData.get(int(id)), "id": int(id)} for id in ids if chipsData.get(int(id))]
    return render_template("cart.html",title="Cart",user=email,products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action","info")
        return redirect(url_for('login')) 
    if add_To_cart(product_id):
        flash("Product added to cart successfully!","success")
    else:
        flash("Product already in cart!","error")
    return redirect(url_for('products'))

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)