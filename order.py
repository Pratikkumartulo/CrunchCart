from flask import session
from db import db
from sqlalchemy.dialects.mysql import JSON
from users import addOrderId

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120))
    contact = db.Column(db.String(10))
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default="Pending")
    price = db.Column(db.Float, nullable=False)

def makeOrder(user_email, contact, street, city, state, zip_code, quantity, item_id,price):
    order = Orders( 
        user_email=user_email,
        contact=contact,
        street=street,
        city=city,
        state=state,
        zip_code=zip_code,
        quantity=quantity,
        price=price,
        item_id=item_id
    )
    db.session.add(order)
    db.session.commit()
    addOrderId(order.id)
    return True

def getOrderById(order_id):
    order = Orders.query.get(order_id)
    if order:
        return {
            "id": order.id,
            "user_email": order.user_email,
            "contact": order.contact,
            "street": order.street,
            "city": order.city,
            "state": order.state,
            "zip_code": order.zip_code,
            "quantity": order.quantity,
            "item_id": order.item_id,
            "timestamp": order.timestamp.strftime('%Y-%m-%d %H:%M:%S') if order.timestamp else None,
            "status": order.status,
            "price": order.price
        }
    return None

def getAllOrders():
    orders = Orders.query.all()
    allOrders = []
    for order in orders:
        temp = {}
        temp['id'] = order.id
        temp['user_email'] = order.user_email
        temp['contact'] = order.contact
        temp['street'] = order.street
        temp['city'] = order.city
        temp['state'] = order.state
        temp['zip_code'] = order.zip_code
        temp['quantity'] = order.quantity
        temp['item_id'] = order.item_id
        temp['timestamp'] = order.timestamp.strftime('%Y-%m-%d %H:%M:%S') if order.timestamp else None
        temp['status'] = order.status
        temp['price'] = order.price
        allOrders.append(temp)
    return allOrders
