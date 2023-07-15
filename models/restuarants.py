from utils.db import db




class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    name_restaurant = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, password,image_url,name_restaurant, description, direccion):
        self.name = name
        self.email = email
        self.name_restaurant = name_restaurant
        self.password = password
        self.image_url = image_url
        self.description = description
        self.direccion = direccion