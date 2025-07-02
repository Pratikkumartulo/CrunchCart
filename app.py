from db import db
from flask import Flask, flash, render_template, redirect, url_for,flash
from forms import SignupForm, LoginForm, OrderForm, CartOrderForm
from chips import chipsData,findMaxThreeDiscount
from users import addUser, getAllUsers,validateUser,addSession,isLoggedIn,logoutUser,add_To_cart,removeFromCart
from order import getOrderById, makeOrder, getAllOrders
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


@app.route('/order/<int:product_id>',methods=['GET', 'POST'])
def order(product_id):
    if product_id not in chipsData:
        flash("Product not found","error")
        return redirect(url_for('products'))
    products = chipsData.get(product_id)
    products['id'] = product_id
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action","info")
        return redirect(url_for('login')) 
    form = OrderForm()
    if form.validate_on_submit():
        makeOrder(
            user_email=email['email'],
            contact=form.contact.data,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            quantity=form.quantity.data,
            item_id=products['id'],
            price=(products['price'] - (products['price'] * products['discount'] / 100)) * int(form.quantity.data) + 40
        )
        flash("Order placed successfully!","success")
        return redirect(url_for('myOrders'))
    return render_template("order.html",title="order",form=form,user=email,product=products)

@app.route('/cart')
def cart():
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action","info")
        return redirect(url_for('login'))
    products=[]
    if(len(email['cart'])!=0):
        ids = email['cart'].split(',')
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

@app.route('/myorders')
def myOrders():
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action", "info")
        return redirect(url_for('login'))
    order_ids = []
    if email['orders']:
        order_ids = [int(id) for id in email['orders'].split(',') if id]
    orders = []
    for id in order_ids:
         order = getOrderById(id)
         if order:
            product = chipsData.get(order['item_id'])
            if product:
                order['product_name'] = product['name']
                order['product_image'] = product['image_url']
                order['product_price'] = product['price']
                order['product_discount'] = product['discount']
                discounted_price = product['price'] - (product['price'] * product['discount'] / 100)
                order['price'] = discounted_price
                order['subtotal'] = discounted_price * order['quantity']
                order['shipping'] = 40
                order['total'] = order['subtotal'] + order['shipping']
                order['address'] = f"{order['street']}, {order['city']}, {order['state']} {order['zip_code']}"
                orders.append(order)
    
    return render_template("myOrders.html", title="My Orders", user=email, orders=orders)


@app.route("/cartorder/place/<cart_string>", methods=["GET","POST"])
def cart_order_place(cart_string):
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action", "info")
        return redirect(url_for('login'))
    form = CartOrderForm()
    if form.validate_on_submit():
        entries = cart_string.split('-')
        for entry in entries:
            try:
                product_id, qty = map(int, entry.split(':'))
                if product_id not in chipsData:
                    flash(f"Product with ID {product_id} not found", "error")
                    continue
                product_price = chipsData.get(product_id)['price']
                product_discount = chipsData.get(product_id)['discount']
                makeOrder(
                    user_email=form.email.data,
                    contact=form.contact.data,
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data,
                    quantity=qty,
                    item_id=product_id,
                    price= (product_price - (product_price * product_discount / 100) * int(qty)) + 40 
                )
            except Exception as e:
                flash(f"Error processing product {entry}: {str(e)}", "error")
                continue
        flash("Order placed successfully!", "success")
        return redirect(url_for('myOrders'))
    return render_template("cartorder.html", title="Cart Order", user=email, cart_string=cart_string, form=form)

@app.get("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    email = isLoggedIn()
    if not email:
        flash("You need to login for this action", "info")
        return redirect(url_for('login'))
    if removeFromCart(product_id):
        flash("Product removed from cart successfully!", "success")
    else:
        flash("Product not found in cart!", "error")
    return redirect(url_for('cart'))

@app.route("/admin")
def admin():
    orders = getAllOrders()
    users = getAllUsers()
    print(orders)
    return render_template('admin.html', title="Admin",orders=orders, users=users)

@app.route("/logout")
def logout():
    logoutUser()
    return redirect(url_for('home'))

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
