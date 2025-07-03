from db import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

def addReview(user_email, item_id, order_id, rating, content):
    review = Review(
        user_email=user_email,
        item_id=item_id,
        order_id=order_id,
        rating=rating,
        content=content
    )
    db.session.add(review)
    db.session.commit()
    return review

def findReviewByOrderId(order_id):
    review = Review.query.filter_by(order_id=order_id).first()
    if review:
        return {
            "user_email": review.user_email,
            "rating": review.rating,
            "content": review.content,
            "item_id": review.item_id,
        }
    return None

def findReviewsByItemId(item_id):
    allReviews = []
    reviews = Review.query.filter_by(item_id=item_id).all()
    for review in reviews:
        allReviews.append({
            "user_email": review.user_email,
            "rating": review.rating,
            "content": review.content,
            "item_id": review.item_id,
        })
    return allReviews

def getReviewByEmail(user_email):
    allReviews = []
    reviews = Review.query.filter_by(user_email=user_email).all()
    for review in reviews:
        allReviews.append({
            "user_email": review.user_email,
            "rating": review.rating,
            "content": review.content,
            "item_id": review.item_id,
        })
    return allReviews
