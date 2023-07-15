from flask import Flask,session

from routes.user import users
from routes.restaurant import restaurants
from routes.product import products
from routes.order import orders
from routes.order_product import orders_products

from decouple import config

import firebase_admin
from firebase_admin import credentials, storage
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


import os





app = Flask(__name__)
cred = credentials.Certificate(config('CREDENCIALES_FIREBASE')) # Ubicación de tu archivo JSON de credenciales de Firebase
firebase_admin.initialize_app(cred, {'storageBucket': config('STORAGR_BUCKET')}) # Aquí coloca el nombre de tu bucket de Firebase Storage




app.config["SQLALCHEMY_DATABASE_URI"] = config('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['WTF_CSRF_ENABLED'] = False
app.permanent_session_lifetime = timedelta(minutes=2)


app.register_blueprint(users)
app.register_blueprint(restaurants)
app.register_blueprint(products)
app.register_blueprint(orders)
app.register_blueprint(orders_products)







