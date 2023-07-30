from flask import Blueprint, request, jsonify, make_response, session
import json

from sqlalchemy.orm import joinedload

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.restuarants import Restaurants
from models.orders import Orders
from models.products import Products

from utils.form_rstaurant import RegiterForm
from utils.form_rstaurant import LoginForm
from utils.security import security

from werkzeug.utils import secure_filename
from firebase_admin import storage 

from utils.db import db

restaurants = Blueprint('restaurants',__name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#registrar restaurant
@restaurants.route('/register/restaurant', methods=['POST'])
def register_restaurant():
    form = RegiterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,  method='scrypt')
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            blob = storage.bucket().blob(filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            blob.make_public()
            image_url = blob.public_url
        else:
            return "Invalid image", 400
        new_user = Restaurants(
                        name=form.name.data, 
                        email=form.email.data,
                        password=hashed_password,
                        image_url=image_url, 
                        name_restaurant=form.name_restaurant.data, 
                        description=form.description.data,
                        direccion=form.direccion.data,
                        )
        try:
            db.session.add(new_user)
            db.session.commit()     
            return make_response(jsonify({"message": "Registered successfully!"}), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
    else:
        return make_response(jsonify({"message": "Form submission invalid"}), 400)

#iniciar sesion restaurant
@restaurants.route('/login/restaurant', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Restaurants.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            encode_token = security.generate_token_restaurant(user)
            response = {
                'message': 'Logged in successfully.',
                'encode_token': encode_token
            }
            return jsonify(response)
        else:
            return jsonify({'message' : 'Invalid email or password.'}), 401
    return jsonify({'message' : 'Invalid form data.'}), 400


#listar todos los pedidos del tal restaurant
@restaurants.route("/api/restaurant/<restaurant_id>/orders/list", methods=['GET'])
def get_restaurant_orders(restaurant_id):
    has_acces = security.verify_token_restaurant(request.headers)
    if has_acces:
            # Obtenemos todas las ordenes del restaurante
            orders = Orders.query.filter_by(restaurant_id=restaurant_id).options(joinedload(Orders.order_products)).all()
            if orders is None:
                return jsonify({'message' : 'No Orders for this restaurant.'}), 401
            # Convertimos los datos a formato JSON
            orders_list = []
            for order in orders:
                # obtenemos los productos de la orden
                products = []
                for order_product in order.order_products:
                    product = Products.query.get(order_product.products_id)
                    products.append({
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'unit': order_product.unit
                    })
                    
                orders_list.append({
                    'id': order.id,
                    'restaurant_id': order.restaurant_id,
                    'user_id': order.user_id,
                    'products': products
                })
            return jsonify(orders_list)
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401

#listar los restaurantes
@restaurants.route("/api/restaurants/list", methods=['GET'])
def get_all_restaurants():
    has_acces = security.verify_token_user(request.headers)
    if has_acces:
        all_restaurants = Restaurants.query.all()
        if not all_restaurants:
            return jsonify({'message' : 'No restaurants found.'}), 404

        restaurants_list = []
        for restaurant in all_restaurants:
            restaurants_list.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'image': restaurant.image_url,
                'name_restaurant': restaurant.name_restaurant,
                'description': restaurant.description,
                'direccion': restaurant.direccion
            })
        
        return jsonify(restaurants_list)
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401