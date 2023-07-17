from flask import Blueprint, request, jsonify, make_response, session
import json
from sqlalchemy import exc
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.users import Users
from models.orders import Orders
from models.order_products import Orders_products
from models.products import Products

from utils.security import security
from utils.forms_user import RegiterForm
from utils.forms_user import LoginForm

from utils.db import db


users = Blueprint('users',__name__)

#registrar usuario
@users.route('/register/user', methods=['POST'])
def register_user():
    form = RegiterForm(request.form)
    print(form.data)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = Users(email=form.email.data, 
                        password=hashed_password, 
                        name=form.name.data, 
                        phone_number=form.phone_number.data)
        try:
            db.session.add(new_user)
            db.session.commit()     
            return make_response(jsonify({"message": "Registered successfully!"}), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
    else:
        return make_response(jsonify({"message": "Form submission invalid"}), 400)

#iniciar sesion usuario
@users.route('/login/user', methods=['POST'])
def login():
    form = LoginForm(request.form)
    print(form.data)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            encode_token = security.generate_token_user(user)
            response = {
                'message': 'Logged in successfully.',
                'encode_token': encode_token
            }
            return jsonify(response)
        else:
            return jsonify({'message' : 'Invalid email or password.'}), 401
    return jsonify({'message' : 'Invalid form data.'}), 400


#usuario genera una orden
@users.route("/api/user/<user_id>/order", methods=['POST'])
def create_order(user_id):
    has_acces = security.verify_token_user(request.headers)
    if has_acces:
        # Obtenemos los datos del formulario
        restaurant_id = request.form.get('restaurant_id')
        products = request.form.getlist('products[]\t')  # 'products[]' debe ser una lista de strings JSON
        print(restaurant_id)
        print(products)
        print(request.form.getlist)
        # Si no se proporcionaron los datos necesarios, retorna un error
        if not restaurant_id or not products:
            return jsonify({'error': 'Missing required fields'}), 400

        # Creamos la orden
        order = Orders(restaurant_id=restaurant_id, user_id=user_id, status=False)

        try:
            # Agregamos y guardamos la orden en la base de datos
            db.session.add(order)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            return jsonify({'error': 'An error occurred when saving the order'}), 500

        # Ahora creamos las entradas en orders_products para cada producto
        for product_str in products:
            # Cada producto es un string JSON que debemos convertir a un diccionario
            product = json.loads(product_str)

            order_product = Orders_products(order_id=order.id, products_id=product['product_id'], unit=product['unit'])

            try:
                # Agregamos y guardamos el producto de la orden en la base de datos
                db.session.add(order_product)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                return jsonify({'error': 'An error occurred when saving the order product'}), 500

        return jsonify({'message': 'Order created successfully'}), 201
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401
    
#obtener la lista de pedidos del usuario
@users.route("/api/user/<user_id>/orders/list", methods=['GET'])
def get_user_orders(user_id):
    # Obtenemos todas las ordenes del usuario
    has_acces = security.verify_token_user(request.headers)
    if has_acces:
        orders = Orders.query.filter_by(user_id=user_id).options(joinedload(Orders.order_products)).all()
        if orders is None:
            return jsonify({'message' : 'No Orders for this user.'}), 401
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
                'status': order.status,
                'products': products
            })
        return jsonify(orders_list)
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401