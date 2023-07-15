from utils.db import db

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship('Restaurants', backref=db.backref('products', lazy=True))

    def __init__(self, name, description, price, image_url , restaurant_id):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.restaurant_id = restaurant_id