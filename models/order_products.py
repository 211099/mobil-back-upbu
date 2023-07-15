from utils.db import db


class Orders_products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Orders', backref=db.backref('order_products', lazy=True))

    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    restaurant = db.relationship('Products', backref=db.backref('order_products', lazy=True))

    unit = db.Column(db.Integer, nullable=False)

    def __init__(self, order_id, products_id, unit):
        self.order_id = order_id
        self.products_id = products_id
        self.unit = unit
        