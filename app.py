from db import db
from flask import Flask, flash, render_template, redirect, url_for,flash
from forms import SignupForm, LoginForm, OrderForm, CartOrderForm, OrderStatusForm, ContactForm, ReviewForm
from chips import chipsData,findMaxThreeDiscount
from review import addReview, findReviewByOrderId, findReviewsByItemId
from contact import addContact, getAllContact
from users import addUser, adminLogin, getAllUsers, isAdmin,validateUser,addSession,isLoggedIn,logoutUser,add_To_cart,removeFromCart,adminLogout
from order import getOrderById, makeOrder, getAllOrders, changeOrderStatus
from config import ADMIN_ID, ADMIN_PASS, DATABASE_URI, SECRET_KEY,SQLALCHEMY_TRACK_MODIFICATIONS

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

@app.route("/contact", methods=['GET', 'POST']) 
def contact():
    form = ContactForm()
    user = isLoggedIn()

    if form.validate_on_submit():
        contact = addContact(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", title="Contact", form=form, user=user)


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
    reviews = findReviewsByItemId(int(id))
    if email:
        chip = chipsData.get(int(id))
        if not chip:
            return redirect(url_for('products'))
        return render_template('product_detail.html',title=f"CrunchCart - {chip['name']}",chipDet = chip,user=email,id=id,reviews=reviews)
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

@app.route("/product/review/<int:order_id>", methods=["GET", "POST"])
def review(order_id):
    user = isLoggedIn()
    if not user:
        flash("Login required to review.", "error")
        return redirect(url_for("login"))

    order = getOrderById(order_id)
    if not order or order['status'].lower() != 'delivered' or order['user_email'] != user['email']:
        flash("Order not found", "error")
        return redirect(url_for("myOrders"))

    item = chipsData.get(order["item_id"])
    form = ReviewForm()

    if form.validate_on_submit():
        addReview(
            user_email=user["email"],
            item_id=order["item_id"],
            order_id=order_id,
            rating=int(form.rating.data),
            content=form.content.data
        )
        flash("Review submitted!", "success")
        return redirect(url_for("myOrders"))

    return render_template("review.html", title="Review Product", form=form, order=order, item=item, user=user)


@app.route('/admin/login', methods=['GET', 'POST'])
def adminsLogin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == ADMIN_ID and form.password.data == ADMIN_PASS:
            adminLogin()
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin'))
    return render_template('adminLogin.html', title="Admin Login", form=form)

@app.route("/admin")
def admin():
    if not isAdmin():
        flash("You are not authorized to access this page.", "error")
        return redirect(url_for('adminsLogin'))
    orders = getAllOrders()
    users = getAllUsers()
    return render_template('admin.html', title="Admin",orders=orders, users=users)

@app.route("/admin/orders")
def adminOrders():
    if not isAdmin():
        flash("You are not authorized to access this page.", "error")
        return redirect(url_for('adminsLogin'))
    orders = getAllOrders()
    return render_template('recentorders.html', title="Admin Orders", orders=orders)

@app.route("/admin/topproducts")
def adminTopProducts():
    if not isAdmin():
        flash("You are not authorized to access this page.", "error")
        return redirect(url_for('adminsLogin'))
    discounted = findMaxThreeDiscount(chipsData)
    return render_template('topproducts.html', title="Top Products", chips=discounted)

@app.route("/admin/allorders")
def AllAdminOrder():
    if not isAdmin():
        flash("You are not authorized to access this page.", "error")
        return redirect(url_for('adminsLogin'))
    orders = getAllOrders()
    return render_template('allorders.html', title="Admin Orders", orders=orders)

@app.route("/admin/order/<int:order_id>", methods=["GET", "POST"])
def adminOrderDetail(order_id):
    if not isAdmin():
        flash("You are not authorized to access this page.", "error")
        return redirect(url_for('adminsLogin'))
    order = getOrderById(order_id)
    review = findReviewByOrderId(order_id)
    item = chipsData.get(order['item_id']) if order else None
    print(item)
    if not order:
        flash("Order not found!", "error")
        return redirect(url_for('adminTopProducts'))

    form = OrderStatusForm()
    if form.validate_on_submit():
        changeOrderStatus(order_id, form.status.data)
        flash("Order status updated successfully!", "success")
        return redirect(url_for("adminOrderDetail", order_id=order_id))

    return render_template("Orderdetails.html", title="Order Detail", order=order, form=form, item=item, review=review)

@app.route("/admin/logout")
def adminsLogout():
    adminLogout()
    flash("Admin logged out successfully!", "success")
    return redirect(url_for('adminsLogin'))

@app.route("/admin/allmessages")
def adminMessages():
    messages = getAllContact()
    return render_template("adminMessage.html", title="All Messages", messages=messages)

@app.route("/logout")
def logout():
    logoutUser()
    return redirect(url_for('home'))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
