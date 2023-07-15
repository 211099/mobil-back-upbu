from utils.db import db


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship('Restaurants', backref=db.backref('orders', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('orders', lazy=True))
    status = db.Column(db.Boolean, nullable=False)

    def __init__(self, restaurant_id, user_id, status):
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        self.status = status
        