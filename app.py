from flask import Flask, flash, render_template,request,jsonify, redirect, url_for,flash,session
from forms import SignupForm, LoginForm
from chips import chipsData,findMaxThreeDiscount
from users import user_data,addUser,validateUser
from datetime import datetime
import json
import os
from werkzeug.security import generate_password_hash
import uuid

app = Flask(__name__)
app.config["SECRET_KEY"] = "15bb914121bfb88e90cd224850b5e614"

orders = []
products = [
    {"id": 1, "name": "Sour Cream & Cheddar", "price": 89.00, "image": "img1.jpg"},
    {"id": 2, "name": "Ginger", "price": 29.00, "image": "img2.jpg"},
    {"id": 3, "name": "Carolina Reaper", "price": 99.00, "image": "img3.jpg"},
    {"id": 4, "name": "Salt & Vinegar", "price": 59.00, "image": "img4.jpg"},
    {"id": 5, "name": "Dill Pickle", "price": 49.00, "image": "img5.jpg"},
    {"id": 6, "name": "Sour Cream & Onion", "price": 79.00, "image": "img6.jpg"},
    {"id": 7, "name": "Barbecue", "price": 109.00, "image": "img7.jpg"},
    {"id": 8, "name": "Chile Limon", "price": 89.00, "image": "img8.jpg"}
]

@app.route("/")
@app.route("/home")
def home():
    discounted = findMaxThreeDiscount(chipsData)
    return render_template("home.html",title="Home",chips = discounted)

@app.route("/about")
def about():
    return render_template("about.html",title="About")

@app.route("/contact") 
def contact():
    return render_template("contact.html",title="contact")


@app.route("/favourites") 
def favourites():
    return render_template("favourites.html",title="favourites",chipsData = chipsData)


@app.route("/products")
def products():
    return render_template("products.html",title="products",chips = chipsData)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if validateUser(form.email.data,form.password.data):
            flash('Login successfull!','success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password','error')

    return render_template('login.html', title="Login", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if addUser(form.username.data,form.email.data,form.gender.data,form.dob.data,form.password.data):
            flash(f'Signup successful! Welcome {form.username.data}!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Email already exists !!','error')
    else:
        flash(f'Some error occured !!','error')

    return render_template('signup.html', title="Signup", form=form)

@app.route("/product/<id>")
def ProductDetail(id):
    print(f"The chip id is {type(id)}")
    chip = chipsData.get(int(id))
    print(chip)
    if not chip:
        return redirect(url_for('products'))
    return render_template('product_detail.html',title=f"CrunchCart - {chip['name']}",chipDet = chip)


@app.route('/order')
def order_page():
    cart = session.get('cart', [])
    cart_items = []
    subtotal = 0

    for item in cart:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': item_total
            })
            subtotal += item_total

    # ✅ Compute required values
    delivery_charge = 2.99 if subtotal < 25 else 0
    tax = round(subtotal * 0.08, 2)
    final_total = round(subtotal + delivery_charge + tax, 2)

    # ✅ Pass all needed values to the template
    return render_template(
        'order.html',
        cart_items=cart_items,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        tax=tax,
        final_total=final_total
    )

    
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if product already in cart
    existing_item = next((item for item in session['cart'] if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        session['cart'].append({'product_id': product_id, 'quantity': quantity})
    
    session.modified = True
    return jsonify({'success': True, 'cart_count': len(session['cart'])})

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    product_id = data.get('product_id')
    
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
        session.modified = True
    
    return jsonify({'success': True})

@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if 'cart' in session:
        for item in session['cart']:
            if item['product_id'] == product_id:
                if quantity > 0:
                    item['quantity'] = quantity
                else:
                    session['cart'].remove(item)
                break
        session.modified = True
    
    return jsonify({'success': True})

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    
    # Generate order ID
    order_id = str(uuid.uuid4())[:8].upper()
    # Calculate order total
    cart = session.get('cart', [])
    order_items = []
    total = 0
    
    for item in cart:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            order_items.append({
                'product_name': product['name'],
                'price': product['price'],
                'quantity': item['quantity'],
                'total': item_total
            })
            subtotal += item_total
    
    delivery_charge = 2.99 if subtotal < 25 else 0
    tax = subtotal * 0.08
    final_total = subtotal + delivery_charge + tax

    
    # Create order
    order = {
        'order_id': order_id,
        'customer_info': data['customer_info'],
        'delivery_address': data['delivery_address'],
        'items': order_items,
        'subtotal': total,
        'delivery_charge':  delivery_charge,
        'tax': tax,
        'total': final_total,
        'payment_method': data['payment_info']['method'],
        'order_date': datetime.now().isoformat(),
        'status': 'Confirmed',
        'estimated_delivery': '30-45 minutes'
    }
    
    orders.append(order)
    
    # Clear cart
    session['cart'] = []
    session.modified = True
    
    return jsonify({
        'success': True, 
        'order_id': order_id,
        'message': 'Order placed successfully!'
    })

@app.route('/order_confirmation/<order_id>')
def order_confirmation(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return redirect(url_for('home'))
    
    return render_template('order_confirmation.html', order=order)

@app.route('/track_order/<order_id>')
def track_order(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order)



if __name__ == "__main__":
    app.run(debug=True)